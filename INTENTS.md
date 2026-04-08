# Intent Registry

> 사용자가 선언하는 의도의 목록. Heartbeat Agent가 주기적으로 읽고 실행한다.
> 의도는 "앞으로 달성할 것", 컨텍스트는 "현재 상태"이다. 혼동하지 않는다.

## 작성 규칙

- 각 Intent는 고유 ID를 가진다: `[카테고리-번호]` (예: monitor-01, dev-02)
- status 변경은 Heartbeat Agent가 자동으로 수행한다 (declared → active → in_progress)
- 사용자가 직접 변경하는 것: 새 Intent 추가, 우선순위 변경, 취소, 완료 확인
- Intent 삭제 대신 archived로 변경한다

---

<!-- 아래부터 Intent 작성 -->

## [monitor-01] Grafana Layer2 프로덕트 품질 지표 수집 복구

- status: completed
- priority: high
- heartbeat: 1h
- permission: L2
- project: ~/workspace/monitoring_personal
- goal: Grafana "Layer 2 - 프로덕트 품질 모니터링" 대시보드의 모든 패널에 데이터가 수집되는 상태
- success_criteria:
  - 메트릭 제공 exporter가 docker-compose에 존재하고 기동 중
  - Prometheus scrape target 상태가 UP
  - 대시보드 패널에서 최근 1시간 데이터 포인트 존재 (No data 없음)
- context:
  - 대시보드 정의: ~/workspace/monitoring_personal/grafana/provisioning/dashboards/layer-product.json
  - 스택 구성: ~/workspace/monitoring_personal/docker-compose.yml
  - Prometheus 설정: ~/workspace/monitoring_personal/prometheus/prometheus.yml
  - 현재 문제: 대시보드가 기대하는 메트릭(http_request_duration_seconds, web_vitals_*, frontend_error_total, aws_rum_*)을 제공하던 Mock Exporter가 docker-compose에서 제거됨
  - Grafana: localhost:3050, Prometheus: localhost:9090
- constraints:
  - 설정 파일 수정은 L1 (자율)
  - docker-compose up/restart는 L2 (승인 필요)
  - 프로덕션 인프라 직접 변경 금지 (L3)
