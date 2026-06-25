from concurrent import futures
from datetime import datetime
import grpc
from opentelemetry.proto.collector.trace.v1 import trace_service_pb2_grpc, trace_service_pb2
LAST_TRACE_RECEIVED = None
TOTAL_TRACE_BATCHES = 0
SPAN_CACHE = {}
class TraceReceiver(trace_service_pb2_grpc.TraceServiceServicer):
    def Export(self, request, context):
        global LAST_TRACE_RECEIVED
        global TOTAL_TRACE_BATCHES
        global SPAN_CACHE
        LAST_TRACE_RECEIVED = datetime.utcnow()
        TOTAL_TRACE_BATCHES += 1
        print("received trace")
        for resource_span in request.resource_spans:
            service_name="NA"
            for attr in resource_span.resource.attributes:
                if attr.key == "service.name": 
                    service_name=attr.value.string_value
            for scope_span in resource_span.scope_spans:
                for span in scope_span.spans:
                    print(service_name, span.name)
                    print(span.span_id.hex(), span.parent_span_id.hex())
                    SPAN_CACHE[span.span_id.hex()] = {"service": service_name, "span_name": span.name, "parent_span": span.parent_span_id.hex(), "timestamp": datetime.utcnow()}
                    create_graph(SPAN_CACHE, span, service_name)
        return trace_service_pb2.ExportTraceServiceResponse()
server=grpc.server(futures.ThreadPoolExecutor(max_workers=11))
trace_service_pb2_grpc.add_TraceServiceServicer_to_server(TraceReceiver(),server)
server.add_insecure_port("[::]:4317")
