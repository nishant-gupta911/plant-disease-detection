import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.BACKEND_URL ?? 'http://127.0.0.1:8000';

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get('file');

    if (!(file instanceof File)) {
      return NextResponse.json(
        { error: 'An image file is required.' },
        { status: 400 }
      );
    }

    const backendFormData = new FormData();
    backendFormData.append('file', file, file.name);

    const response = await fetch(`${BACKEND_URL}/predict`, {
      method: 'POST',
      body: backendFormData,
      cache: 'no-store',
    });

    const payload = await response.json().catch(() => null);

    if (!response.ok) {
      return NextResponse.json(
        {
          error:
            payload?.detail ??
            payload?.error ??
            `Backend prediction failed with status ${response.status}.`,
        },
        { status: response.status }
      );
    }

    return NextResponse.json(payload, { status: 200 });
  } catch (error) {
    return NextResponse.json(
      {
        error:
          error instanceof Error
            ? error.message
            : 'Could not connect to the prediction service.',
      },
      { status: 503 }
    );
  }
}
