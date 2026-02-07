import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import FileResponse
from .models import Dataset
from .pdf_utils import generate_report_pdf

# Temporary storage for last uploaded summary (for PDF generation)
LAST_SUMMARY = None


@api_view(['POST'])
def upload_csv(request):
    global LAST_SUMMARY

    file = request.FILES.get('file')

    if not file:
        return Response({"error": "No file uploaded"}, status=400)

    try:
        df = pd.read_csv(file)
    except Exception:
        return Response({"error": "Invalid CSV file"}, status=400)

    summary = {
        "total_count": int(len(df)),
        "average_flowrate": float(df["Flowrate"].mean()),
        "average_pressure": float(df["Pressure"].mean()),
        "average_temperature": float(df["Temperature"].mean()),
        "equipment_type_distribution": df["Type"].value_counts().to_dict()
    }

    # Save to database
    Dataset.objects.create(
        filename=file.name,
        summary=summary
    )

    # Keep only last 5 datasets
    if Dataset.objects.count() > 5:
        Dataset.objects.order_by("uploaded_at").first().delete()

    # Store summary for PDF generation
    LAST_SUMMARY = summary

    return Response(summary)


@api_view(['GET'])
def upload_history(request):
    datasets = Dataset.objects.order_by("-uploaded_at")[:5]

    history = []
    for d in datasets:
        history.append({
            "filename": d.filename,
            "uploaded_at": d.uploaded_at,
            "summary": d.summary
        })

    return Response(history)


@api_view(['GET'])
def download_pdf_report(request):
    global LAST_SUMMARY

    if LAST_SUMMARY is None:
        return Response(
            {"error": "No data available. Upload CSV first."},
            status=400
        )

    pdf_buffer = generate_report_pdf(LAST_SUMMARY)

    return FileResponse(
        pdf_buffer,
        as_attachment=True,
        filename="chemical_equipment_report.pdf"
    )
