---
name: "disk-cleanup-audit"
description: "디스크 정리 요청 시 대형 경로와 안전한 캐시·로그·중복 Snap을 분류하고 검증 가능한 결과를 만든다."
---

# Disk Cleanup Audit

**목차** · [절차](#절차) · [완료 기준](#완료-기준)

## 절차

1. **현재 상태를 기록한다.** df -h /로 전체·사용량·여유 공간을 확인하고, /tmp와 OpenClaw workspace의 용량을 별도로 기록한다. 정리 전 수치를 보존했으면 완료다.

2. **큰 경로와 파일을 읽기 전용으로 찾는다.** /home/ubuntu, /var, /opt를 같은 파일시스템 범위에서 du로 확인하고, 500MB보다 큰 파일을 별도로 찾는다. 결과를 캐시·로그·임시 산출물·활성 데이터로 분류했으면 완료다.

3. **OpenClaw 임시자료를 분리한다.** /home/ubuntu/.openclaw/tmp 아래에서 임시 캡처의 용량과 경로를 확인한다. /home/ubuntu/.openclaw/media는 inbound, tool-image-generation, tool-video-generation, generated, browser, outbound로 나눠 확인한다. inbound는 사용자 첨부 원본일 수 있으므로 별도 승인 없이는 삭제 후보에 넣지 않는다.

4. **삭제 범위를 확인한다.** 사용자가 “정리”라고만 하면 즉시 삭제하지 말고 후보를 제시한다. 사용자가 우선 후보와 중복 Snap을 명시적으로 승인했으면 그 범위만 실행하고, 미디어 전체는 명시적으로 승인될 때까지 보류한다.

5. **작업자료는 먼저 복구 가능한 곳으로 이동한다.** OpenClaw 임시 캡처처럼 사용자 원본이 아닌 항목은 /home/ubuntu/workspace/knowledge-lab/source/openclaw-system/trash/disk-cleanup-YYYYMMDD/로 이동한다. 사용자가 휴지통 비우기를 명시하면 해당 날짜 폴더만 비우고 잔여 여부를 확인한다.

6. **캐시와 로그를 정리한다.** 승인된 경우 npm cache clean --force, sudo -n apt-get clean, sudo -n journalctl --vacuum-size=200M를 실행한다. 권한이 없으면 정리 완료로 말하지 말고 실패 원인을 남긴다.

7. **중복 Snap을 식별해 제거한다.** snap list --all에서 disabled 리비전만 대상으로 삼고, 패키지명과 리비전을 확인한 뒤 sudo -n snap remove <name> --revision=<revision>을 실행한다. disabled 잔여 목록이 없어졌는지 확인한다. 활성 리비전은 건드리지 않는다.

8. **브라우저와 미디어는 보수적으로 다룬다.** browser는 실행 중일 수 있으므로 전체 삭제하지 않는다. inbound는 사용자 첨부일 수 있어 보존한다. tool-image-generation과 generated는 생성 결과일 수 있으므로 보존 여부를 확인받는다. outbound와 오래된 tool-video-generation은 별도 승인 후 정리한다.

9. **정리 후 수치를 검증한다.** 다시 df -h /와 정리 대상별 du -sh를 실행한다. 사용률 변화, 남은 대상, 미디어 보류 범위를 보고하고, 삭제하지 않은 항목을 삭제 완료처럼 표현하지 않는다.

10. **자동화 상태를 따로 확인한다.** 사용자가 디스크 정리 크론의 작동 여부를 묻으면 자동화 목록에서 이름·활성화·최근 실행 결과를 확인한다. 이름에 disk, cleanup, temp, storage가 없거나 후보가 없으면 디스크 정리 크론이 확인되지 않았다고 보고하며 새 크론을 임의로 만들지 않는다.

## 완료 기준

- 정리 전후 디스크 수치가 기록되어 있다.
- 승인 범위 밖의 사용자 첨부·활성 데이터·활성 Snap은 보존되어 있다.
- 캐시·로그·disabled Snap의 처리 결과와 권한 실패가 구분되어 있다.
- 휴지통 이동·비우기 결과와 잔여 경로가 검증되어 있다.
- 디스크 정리 자동화의 존재 여부를 실제 목록과 최근 실행 결과로 확인했다.
