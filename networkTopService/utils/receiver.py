from concurrent import futures
from datetime import datetime
import grpc
from opentelemetry.proto.collector.trace.v1 import trace_service_pb2_grpc, trace_service_pb2
LAST_TRACE_RECEIVED = None
TOTAL_TRACE_BATCHES = 0
class TraceReceiver(trace_service_pb2_grpc.TraceServiceServicer):
    def Export(self, request, context):
        global LAST_TRACE_RECEIVED
        global TOTAL_TRACE_BATCHES
        LAST_TRACE_RECEIVED = datetime.utcnow()
        TOTAL_TRACE_BATCHES += 1
        print("received trace")
        for resource_span in request.resource_spans:
            print(resource_span)
            service_name="NA"
            for attr in resource_span.resource.attributes:
                if attr.key == "service.name": 
                    service_name=attr.value.string_value
            for scope_span in resource_span.scope_spans:
                for span in scope_span.spans:
                    print(service_name, span.name)
                    print(span.span_id.hex(), span.parent_span_id.hex())
        return trace_service_pb2.ExportTraceServiceResponse()
server=grpc.server(futures.ThreadPoolExecutor(max_workers=11))
trace_service_pb2_grpc.add_TraceServiceServicer_to_server(TraceReceiver(),server)
server.add_insecure_port("[::]:4317")
