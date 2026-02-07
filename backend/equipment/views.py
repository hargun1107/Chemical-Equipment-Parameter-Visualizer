import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Dataset

@api_view(['POST'])
def upload_csv(request):
    file = request.FILES.get('file')

    if not file:
        return Response({"error": "No file uploaded"}, status=400)

    df = pd.read_csv(file)

    summary = {
        "total_count": len(df),
        "average_flowrate": df["Flowrate"].mean(),
        "average_pressure": df["Pressure"].mean(),
        "average_temperature": df["Temperature"].mean(),
        "equipment_type_distribution": df["Type"].value_counts().to_dict()
    }

    Dataset.objects.create(
        filename=file.name,
        summary=summary
    )

    if Dataset.objects.count() > 5:
        Dataset.objects.order_by('uploaded_at').first().delete()

    return Response(summary)


@api_view(['GET'])
def upload_history(request):
    datasets = Dataset.objects.order_by('-uploaded_at')[:5]
    return Response([
        {
            "filename": d.filename,
            "uploaded_at": d.uploaded_at,
            "summary": d.summary
        } for d in datasets
    ])
