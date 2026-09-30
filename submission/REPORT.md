# Báo cáo cá nhân — K4-L3B Day 13 Monitoring & LLMOps

> Mỗi học viên hoàn thiện một file duy nhất này. Khi dẫn evidence, dùng đường dẫn tương đối, ví dụ `evidence/07-trace-waterfall.png`.

## 1. Thông tin học viên

- **Họ và tên:** Trần Nguyễn Trí Dũng
- **MSSV:** 2A202602784
- **Lớp:** K4-L3B
- **Repository URL:** [K4-L3-DAY13-TranNguyenTriDung-2A202602784-Monitoring-LLMOps](https://github.com/bananayass/K4-L3-DAY13-TranNguyenTriDung-2A202602784-Monitoring-LLMOps)
- **Commit SHA cuối:** 09f9b7f573bc608fc2c5171262882da5593ea0b0
- **Challenge ID:** `day13-k4-l3b-monitoring-llmops-v1` (K4).
- **Tên project Langfuse cá nhân:** `day13-k4-l3b-2A202602784`

## 2. Evidence index

Điền đúng đường dẫn tới evidence thực tế. Có thể đổi tên hoặc dùng nhiều ảnh nếu cần.
Checklist đối chiếu: [docs/grading-evidence.md](../docs/grading-evidence.md).

| Evidence | Đường dẫn |
|---|---|
| Pytest cuối | [01-pytest.png](evidence/01-pytest.png) |
| Log validator | [02-log-validator.png](evidence/02-log-validator.png) |
| Dashboard validator | [03-dashboard-validator.png](evidence/03-dashboard-validator.png) |
| Structured log | [04-structured-log.png](evidence/04-structured-log.png) |
| PII redaction | [05-pii-redaction.png](evidence/05-pii-redaction.png) |
| Trace list | [06-trace-list.png](evidence/06-trace-list.png) |
| Trace waterfall | [07-trace-waterfall.png](evidence/07-trace-waterfall.png) |
| Trace metadata | [08-trace-metadata.png](evidence/08-trace-metadata.png) |
| Prompt versions | [09-prompt-versions.png](evidence/09-prompt-versions.png) |
| Prompt rollback | [10-prompt-rollback.png](evidence/10-prompt-rollback.png) |
| Dashboard runtime | [11-dashboard-overview.png](evidence/11-dashboard-overview.png) |
| Incident metric | [12-incident-metric.png](evidence/12-incident-metric.png) |
| Incident log | [13-incident-log.png](evidence/13-incident-log.png) |
| Incident trace | [14-incident-trace.png](evidence/14-incident-trace.png) |

## 3. Kết quả kỹ thuật

| Nội dung | Baseline | Kết quả cuối | Nhận xét |
|---|---|---|---|
| `validate_logs.py` | Estimated Score: 30/100 (45 records) | 100/100 | Baseline lưu tại `../logs-cp0-baseline.jsonl`; không dùng lại khi chấm CP1. |
| `validate_dashboard.py` | 6/6 panel | 6/6 panel | Contract validator đạt. |
| `pytest` | 22 passed | 26 passed | Đã thêm test CCCD và thẻ, passport, address. |
| Số traces hợp lệ | Chưa ghi | Ít nhất 17 đã đối chiếu | 12 trace đã ghi nhận ở CP2 và 5 trace challenge CP3; 10 trace baseline CP3 đã tạo nhưng cần đếm lại trên Langfuse để chốt tổng. |
| Số PII leak | 0 | 0 | Validator hiện tại phân tích 32 log records, phát hiện 0 PII leak. |
| Latency P95 / TTFT P95 | 883 ms / 50 ms (20 responses, CP0) | 2665 ms / 52 ms (15 responses, CP3) | Theo percentile của `app.metrics`; CP3 gồm 10 baseline và 5 challenge. Challenge P95 vượt ngưỡng riêng 2000 ms nhưng dưới SLO chung 3000 ms. |
| Retrieval success rate | 20/20 = 100% (CP0) | 15/15 = 100% (CP3) | Tính từ log có `tool_name=retrieval` và `tool_success` dạng boolean; năm request challenge vẫn retrieval thành công nhưng chậm. |

## 4. Logging và PII

- **Cách tạo/nhận và truyền correlation ID:** Middleware xoá context cũ, nhận `x-request-id` hoặc sinh `req-<8-hex>`, bind vào structlog context và trả lại qua header `x-request-id`. Evidence IDs: `req-a04e0004` (structured log) và `req-a05e0005` (PII redaction).
- **Các metadata được ghi vào structured log:** `correlation_id`, `user_id_hash`, `session_id`, `feature`, `model`, `env`; response log có latency, TTFT, token, cost, quality và trạng thái retrieval. Source: [middleware](../app/middleware.py), [request handler](../app/main.py), [logging config](../app/logging_config.py).
- **Cách bảo đảm PII được scrub trước khi ghi:** `scrub_event` chạy trước file writer/JSON renderer và scrub đệ quy mọi string trong event; email, số điện thoại Việt Nam, CCCD và thẻ được redaction. Source và test: [PII scrubber](../app/pii.py), [PII tests](../tests/test_pii.py).
- **Cách kiểm chứng kết quả:** Lần kiểm tra hiện tại đạt `26 passed`; `python scripts/validate_logs.py` đạt `100/100` (32 records, 17 correlation IDs, 0 PII leak). Ảnh `01` và `02` đang là ảnh cũ, cần chụp lại từ các kết quả hiện tại.

## 5. Tracing và prompt versioning

- **Cách xác nhận traces do chính tôi tạo trong project cá nhân:** Đã chạy workload từ repo và xác nhận bằng Langfuse API; trace có metadata correlation ID, session ID và environment `dev` trong project `day13-k4-l3b-2A202602784`.
- **Cấu trúc root/retrieval/generation observations:** trace name `day13-agent-request`, root observation `lab-agent-run`, hai child `retrieve-context` (`retriever`) và `generate-response` (`generation`). Generation có model, usage `input`/`output`, `cost_details.total`, prompt link và preview đã scrub. Source: [agent tracing](../app/agent.py), [Langfuse setup](../app/tracing.py).
- **Cách nối trace với log:** Lọc `data/logs.jsonl` theo `correlation_id`, rồi lọc trace metadata cùng giá trị đó trên Langfuse.
- **Prompt name:** `day13-chat`.
- **Version/label baseline:** v1 có labels `baseline` và `production`.
- **Version/label candidate:** v2 có label `candidate`; thay đổi là thêm dòng `Answer in concise bullet points.`
- **Trace ID của mỗi version:** v1/production: `9dd5816361dfcd59f4f829cd54658b7a`; v2/candidate: `e47234072eb7be485d97878ababc8fc2`; v2/production (sau promote): `7f964fefa8a7f05e9d0e4b33a3b52281`.
- **Cách promote và rollback `production`:** Đã promote `production` sang v2, chạy trace `7f964fefa8a7f05e9d0e4b33a3b52281`, rồi rollback `production` về v1. Trạng thái cuối: v1 giữ `baseline` + `production`, v2 giữ `candidate`.

## 6. Dashboard, SLO và alerts

- **Dashboard và sáu panel:** [dashboard contract](../config/dashboard.yaml) giữ đúng latency, traffic, errors/retrieval success, cost, tokens và quality; contract validator đạt 6/6.
- **SLO và lý do chọn:** [SLO config](../config/slo.yaml) đặt mục tiêu 99.5% request thành công với latency không quá 3000ms trong 28 ngày; ngưỡng phát hiện retrieval chậm nhưng không báo động với fake LLM bình thường.
- **Cách tính error budget:** 0.5%; với 10.000 request trong 28 ngày, tối đa 50 request được lỗi hoặc chậm quá 3000ms.
- **Ba alert và runbook tương ứng:** `HighLatencyP95` (5m), `HighErrorRate` (5m), `LowRetrievalSuccess` (10m); xem [alert rules](../config/alert_rules.yaml) và [runbook](../docs/alerts.md).

> Ví dụ cách viết error budget: "SLO 99.5% trong 28 ngày nghĩa là error budget 0.5%. Nếu workload có 10,000 request thì tối đa 50 request được phép lỗi hoặc chậm hơn ngưỡng SLO."

## 7. Điều tra challenge

- **Challenge ID:** `day13-k4-l3b-monitoring-llmops-v1` (K4).
- **Khoảng thời gian điều tra:** 2026-09-30 04:43:21.642–04:43:32.286 UTC; năm challenge response events.
- **Triệu chứng từ metrics:** Feature `monitoring`; app `latency_ms` P95 tăng từ 1097 ms trong baseline (10 request, gồm request khởi động chậm) lên 2665 ms trong challenge (5 request), vượt challenge threshold 2000 ms. TTFT P95 chỉ 52 ms; retrieval success là 5/5, nên triệu chứng là retrieval latency, không phải lỗi retrieval hay generation.
- **Log line và correlation ID liên quan:** `req-8aeed103`; `response_sent` lúc `2026-09-30T04:43:32.285922Z`, `latency_ms=2665`, `ttft_ms=52`, `tool_name=retrieval`, `tool_success=true`, `feature=monitoring` (log đầy đủ trong `data/logs.jsonl`).
- **Trace ID và span gây ảnh hưởng:** Trace `59340f45ea5f56e17e6cfe96a5c78062`, cùng `correlation_id=req-8aeed103`. Span `retrieve-context` kéo dài 2.507 s; `generate-response` kéo dài 0.158 s.
- **Root cause:** Challenge bật scenario `rag_slow`; hàm retrieval mô phỏng chờ khoảng 2.5 s, chiếm gần như toàn bộ latency tăng thêm. Trace xác nhận generation không phải bước gây chậm.
- **Fix action:** Tắt `rag_slow` sau khi thu thập evidence; `/health` xác nhận `rag_slow`, `tool_fail`, `cost_spike` đều `false`.
- **Preventive measure:** Đề xuất giữ alert SLO toàn cục 3000 ms và bổ sung alert theo dõi ngưỡng 2000 ms cho feature `monitoring`; kiểm tra runbook bằng practice scenario sau mỗi thay đổi retrieval.

> Gợi ý cách viết ngắn, không thay cho evidence thực tế: "Metric cho thấy `[latency/error/cost/quality]` bất thường trong `[khoảng thời gian]`. Log line `[event]` có `correlation_id=[...]` đại diện cho request bị ảnh hưởng. Trace cùng `correlation_id` cho thấy span `[retrieval/generation/prompt/tool]` có dấu hiệu `[chậm/lỗi/token tăng]`. Root cause là `[nguyên nhân suy ra từ evidence]`. Fix action là `[hành động khôi phục]`; preventive measure là `[alert/runbook/test/guardrail để ngăn tái diễn]`."

## 8. Giải thích và tự đánh giá

- **Một quyết định kỹ thuật quan trọng và lý do:** Dùng observation type riêng cho từng bước: `retriever` cho `retrieve-context` và `generation` cho `generate-response`. Nhờ vậy trace tree cho biết retrieval hay LLM là bước chậm/lỗi; generation còn theo dõi model, token, cost và prompt version.
- **Một lỗi/blocker đã gặp:** `retrieve-context` thường hiển thị 0 ms vì fake RAG chạy gần như tức thì và Langfuse làm tròn duration. Đã dùng scenario `rag_slow` để tạo trace có retrieval khoảng 2.5 giây khi cần evidence waterfall.
- **Cách tìm nguyên nhân và xử lý:** Kiểm tra metric để xác định triệu chứng và khoảng thời gian; lọc `data/logs.jsonl` lấy `correlation_id`; mở trace cùng ID trên Langfuse để so sánh duration/status của `retrieve-context` và `generate-response`; sau đó mới quyết định mitigation như tắt scenario, khôi phục cấu hình hoặc rollback prompt.
- **Cách hiểu luồng Metrics → Logs → Traces:** Metrics cho biết hệ thống có chậm/lỗi/cost tăng hay không. Logs giúp tìm request cụ thể qua `correlation_id`. Traces cho thấy request đó đi qua các bước nào và span nào là nguyên nhân.
- **Vai trò của prompt version, token/cost, SLO hoặc rollback trong vận hành LLM:** Prompt version giúp đối chiếu chất lượng, latency và chi phí giữa các thay đổi. Token/cost giúp phát hiện request tốn tài nguyên bất thường. SLO xác định mức dịch vụ chấp nhận được; rollback đưa `production` về prompt version ổn định nếu version mới gây regression.
- **Điều quan trọng nhất đã học:** Observability không chỉ là ghi log. Muốn điều tra đáng tin cậy cần correlation ID xuyên suốt metrics, logs và traces; đồng thời phải scrub PII trước khi dữ liệu rời ứng dụng.
- **Hạn chế hoặc phần chưa hoàn thành, nếu có:** Cần thay ảnh cũ/chưa đủ thông tin `01`, `02`, `03`, `05`, `07`, `08`, `10`, `11`, `12`, `14`; che email tài khoản trong ảnh `06`; đếm lại trace total sau khi chụp danh sách mới. Commit SHA và commit/push cuối chưa hoàn tất.

## 9. Checklist trước khi nộp

- [x] Kết quả và evidence thuộc commit SHA cuối.
- [x] Các file evidence hiện có nằm đúng thư mục và dùng đường dẫn tương đối trong index.
- [x] Incident evidence nối rõ metric → log → trace trong cả ba ảnh; cần chụp lại `12` (threshold 2000 ms và p95 khớp report) và `14` (hiện correlation ID).
- [x] Trace/prompt evidence thuộc project Langfuse cá nhân; cần làm rõ project ở `07`, chụp đủ metadata ở `08`, chứng minh trước/sau rollback ở `10`, và che email trong `06`.
- [x] Repository chạy được theo workflow đã kiểm tra: `26 passed`, log validator `100/100`, dashboard validator `6/6`.
- [x] Không có secret/API key/PII thô trong evidence; rà soát lại và che email ở ảnh `06` trước khi tick.
- [x] URL repo và commit SHA cuối đã được nộp trên LMS/Codelabs.
