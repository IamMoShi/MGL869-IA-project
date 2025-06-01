from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.metrics import set_meter_provider, get_meter_provider
from opentelemetry.sdk.metrics import Meter

name = "fastAPI.model-training"

# 1. Configure resource
resource = Resource.create(attributes={SERVICE_NAME: name})

# 2. Set up the exporter and reader
metric_reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(
        endpoint="http://localhost:4317/v1/metrics",
        insecure=True
    ),
    export_interval_millis=500
)

# 3. Create and set MeterProvider BEFORE calling get_meter_provider or get_meter
provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
set_meter_provider(provider)

# 4. Now it's safe to access meters
meter = get_meter_provider().get_meter(name)

training_progress = meter.create_gauge("training_progress")
