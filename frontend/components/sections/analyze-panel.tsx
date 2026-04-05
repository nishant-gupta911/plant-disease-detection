'use client';

import { useEffect, useMemo, useState } from 'react';
import { AlertCircle, ClipboardPaste, ImagePlus, Leaf, LoaderCircle, Upload } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

type PredictionItem = {
  class: string;
  confidence: number;
};

type PredictResponse = {
  predicted_class: string | null;
  confidence: number;
  top_3_predictions?: PredictionItem[];
  top_5?: [string, number][];
  message?: string;
  error?: string;
};

const fallbackPredictions: PredictionItem[] = [
  { class: 'Tomato Early Blight', confidence: 0.83 },
  { class: 'Tomato Septoria Leaf Spot', confidence: 0.12 },
  { class: 'Healthy Leaf', confidence: 0.05 },
];

export function AnalyzePanel() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [prediction, setPrediction] = useState<PredictResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);

  const chartItems = useMemo(() => {
    if (!prediction) {
      return fallbackPredictions;
    }

    if (prediction.top_3_predictions?.length) {
      return prediction.top_3_predictions;
    }

    if (prediction.top_5?.length) {
      return prediction.top_5.slice(0, 3).map(([diseaseClass, confidence]) => ({
        class: diseaseClass,
        confidence,
      }));
    }

    return [
      {
        class: prediction.predicted_class,
        confidence: prediction.confidence,
      },
    ];
  }, [prediction]);

  const handleFileChange = (selectedFile: File | null) => {
    setFile(selectedFile);
    setPrediction(null);
    setError(null);
  };

  useEffect(() => {
    if (!file) {
      setPreviewUrl(null);
      return;
    }

    const objectUrl = URL.createObjectURL(file);
    setPreviewUrl(objectUrl);

    return () => URL.revokeObjectURL(objectUrl);
  }, [file]);

  const extractImageFile = (files: FileList | File[] | null | undefined) => {
    if (!files) {
      return null;
    }

    return Array.from(files).find((candidate) =>
      candidate.type.startsWith('image/')
    ) ?? null;
  };

  const handlePaste = async () => {
    try {
      const clipboardItems = await navigator.clipboard.read();
      for (const item of clipboardItems) {
        const imageType = item.types.find((type) => type.startsWith('image/'));
        if (imageType) {
          const blob = await item.getType(imageType);
          const pastedFile = new File([blob], 'pasted-leaf.png', { type: imageType });
          handleFileChange(pastedFile);
          return;
        }
      }
      setError('Clipboard does not contain an image yet.');
    } catch {
      setError('Clipboard image paste needs browser permission. You can also drag and drop a file.');
    }
  };

  useEffect(() => {
    const onPaste = (event: ClipboardEvent) => {
      const pastedImage = extractImageFile(event.clipboardData?.files);
      if (pastedImage) {
        event.preventDefault();
        handleFileChange(pastedImage);
      }
    };

    window.addEventListener('paste', onPaste);
    return () => window.removeEventListener('paste', onPaste);
  }, []);

  const onDrop = (event: React.DragEvent<HTMLLabelElement>) => {
    event.preventDefault();
    setDragActive(false);
    const droppedImage = extractImageFile(event.dataTransfer.files);
    if (droppedImage) {
      handleFileChange(droppedImage);
    } else {
      setError('Please drop an image file.');
    }
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please upload a plant leaf image before analyzing.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('/api/predict', {
        method: 'POST',
        body: formData,
      });

      const payload = (await response.json()) as PredictResponse & { error?: string };

      if (!response.ok) {
        setPrediction({
          predicted_class: 'Tomato Early Blight',
          confidence: 0.83,
          top_3_predictions: fallbackPredictions,
        });
        setError(
          payload.error ??
            'The prediction service is unavailable right now, so a sample response is shown instead.'
        );
        return;
      }

      setPrediction(payload);
      if (payload.message) {
        setError(payload.message);
      }
    } catch {
      setPrediction({
        predicted_class: 'Tomato Early Blight',
        confidence: 0.83,
        top_3_predictions: fallbackPredictions,
      });
      setError(
        'The prediction service could not be reached, so a sample response is shown for the UI preview.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid gap-8 lg:grid-cols-[1.1fr_0.9fr]">
      <div className="rounded-[2rem] border border-border/60 bg-card/90 p-6 shadow-xl shadow-lime-900/5 dark:shadow-black/20">
        <div className="flex items-center gap-3">
          <div className="rounded-full bg-primary/10 p-3 text-primary">
            <Upload className="size-5" />
          </div>
          <div>
            <p className="text-lg font-semibold">Upload a leaf image</p>
            <p className="text-sm text-muted-foreground">
              JPG, PNG, or WEBP images work best with clear lesion detail.
            </p>
          </div>
        </div>

        <label
          className={cn(
            'mt-6 flex min-h-80 cursor-pointer flex-col items-center justify-center rounded-[1.5rem] border border-dashed border-primary/30 bg-gradient-to-br from-lime-50 to-emerald-50 p-6 text-center transition hover:border-primary/50 dark:from-slate-900 dark:to-emerald-950/60',
            dragActive && 'scale-[1.01] border-primary bg-primary/5'
          )}
          onDragEnter={(event) => {
            event.preventDefault();
            setDragActive(true);
          }}
          onDragOver={(event) => {
            event.preventDefault();
            setDragActive(true);
          }}
          onDragLeave={(event) => {
            event.preventDefault();
            setDragActive(false);
          }}
          onDrop={onDrop}
        >
          {previewUrl ? (
            <img
              src={previewUrl}
              alt="Leaf preview"
              className="h-full max-h-72 w-full rounded-[1.25rem] object-cover"
            />
          ) : (
            <>
              <ImagePlus className="size-10 text-primary" />
              <p className="mt-4 text-lg font-medium">Drag and drop, paste, or click to browse</p>
              <p className="mt-2 max-w-sm text-sm text-muted-foreground">
                Capture the full leaf under natural light, then drop it here or press `Ctrl/Cmd + V`.
              </p>
            </>
          )}
          <input
            type="file"
            accept="image/*"
            className="hidden"
            onChange={(event) => handleFileChange(event.target.files?.[0] ?? null)}
          />
        </label>

        <div className="mt-6 flex flex-col gap-3 sm:flex-row">
          <Button onClick={handleAnalyze} size="lg" className="rounded-full px-6">
            {loading ? <LoaderCircle className="mr-2 size-4 animate-spin" /> : <Leaf className="mr-2 size-4" />}
            Analyze Image
          </Button>
          <Button
            type="button"
            variant="secondary"
            size="lg"
            className="rounded-full px-6"
            onClick={handlePaste}
          >
            <ClipboardPaste className="mr-2 size-4" />
            Paste Image
          </Button>
          <Button
            type="button"
            variant="outline"
            size="lg"
            className="rounded-full px-6"
            onClick={() => handleFileChange(null)}
          >
            Reset
          </Button>
        </div>

        {error ? (
          <div className="mt-4 flex items-start gap-3 rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800 dark:border-amber-900/60 dark:bg-amber-950/40 dark:text-amber-200">
            <AlertCircle className="mt-0.5 size-4 shrink-0" />
            <p>{error}</p>
          </div>
        ) : null}
      </div>

      <div className="space-y-6">
        <div className="rounded-[2rem] border border-border/60 bg-slate-950 p-6 text-white shadow-xl">
          <p className="text-sm uppercase tracking-[0.2em] text-lime-300/70">Prediction</p>
          <p className="mt-4 text-3xl font-semibold">
            {prediction?.predicted_class ?? (prediction ? 'No confident match' : 'Awaiting analysis')}
          </p>
          <p className="mt-3 text-sm text-slate-300">
            {prediction
              ? `Confidence score: ${(prediction.confidence * 100).toFixed(2)}%`
              : 'Upload an image to inspect disease confidence and ranked matches.'}
          </p>
        </div>

        <div className="rounded-[2rem] border border-border/60 bg-card/90 p-6 shadow-xl shadow-lime-900/5 dark:shadow-black/20">
          <div className="flex items-center justify-between">
            <p className="text-lg font-semibold">Top matches</p>
            <p className="text-sm text-muted-foreground">Model confidence</p>
          </div>
          <div className="mt-6 space-y-4">
            {chartItems.map((item) => (
              <div key={item.class}>
                <div className="mb-2 flex items-center justify-between text-sm">
                  <span className="font-medium">{item.class}</span>
                  <span className="text-muted-foreground">
                    {(item.confidence * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="h-3 overflow-hidden rounded-full bg-muted">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-primary to-emerald-500"
                    style={{ width: `${Math.max(item.confidence * 100, 6)}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
