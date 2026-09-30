# Alert và runbook

Các alert dựa trên triệu chứng người dùng thấy được. Khi điều tra, luôn đi theo Metrics → Logs → Traces, không đoán nguyên nhân từ tên incident.

## HighLatencyP95

- Severity: `warning`; duration: `5m`; channel: Slack `#k4-l3b-alerts`; owner: `student-2A202602784`.
- Điều kiện: P95 của `response_sent.latency_ms` lớn hơn `3000ms` liên tục 5 phút.
- Ảnh hưởng: người dùng chờ câu trả lời lâu.
- Kiểm tra: (1) xác nhận P95/P99 và TTFT trên panel latency; (2) lấy `correlation_id` có latency cao trong `data/logs.jsonl`; (3) mở trace cùng ID và so sánh `retrieve-context` với `generate-response`.
- Mitigation: tắt practice scenario gây chậm hoặc rollback prompt/config vừa đổi sau khi evidence xác nhận.

## HighErrorRate

- Severity: `critical`; duration: `5m`; channel: Slack `#k4-l3b-alerts`; owner: `student-2A202602784`.
- Điều kiện: `request_failed / request_received` lớn hơn `2%` liên tục 5 phút.
- Ảnh hưởng: người dùng không nhận được câu trả lời.
- Kiểm tra: (1) xác nhận error rate theo thời gian; (2) lọc event `request_failed`, nhóm theo `error_type` và lấy correlation ID; (3) mở trace cùng ID để xác định retrieval hay generation lỗi.
- Mitigation: tắt scenario lỗi, khôi phục dependency/config trước thay đổi, sau đó chạy một request kiểm chứng.

## LowRetrievalSuccess

- Severity: `warning`; duration: `10m`; channel: Slack `#k4-l3b-alerts`; owner: `student-2A202602784`.
- Điều kiện: tỷ lệ `tool_success=true` của retrieval nhỏ hơn `90%` liên tục 10 phút.
- Ảnh hưởng: câu trả lời thiếu context hoặc request thất bại.
- Kiểm tra: (1) xác nhận retrieval-success rate ở panel errors; (2) lọc log có `tool_name=retrieval` và `tool_success=false`; (3) so sánh `retrieve-context` của trace lỗi với trace thành công.
- Mitigation: tắt scenario retrieval lỗi, kiểm tra vector-store/config corpus, rồi chạy workload lại.
