# product-01 · 배포 결정 가이드

> intent: `product-01`
> created: 2026-05-14 (heartbeat prepare)
> 후보 도메인: `virtue.oracle.shdkej.com`

## 결론 (TL;DR)

**oracle 서버 자체 호스팅 권장.**

`oracle.shdkej.com` 서버는 이미 `infinity.oracle.shdkej.com`을 운영 중이다. 같은 서버에 PM2 + Nginx 역방향 프록시로 `virtue.oracle.shdkej.com`을 추가하면 인프라 추가 없이 배포 가능. 단, ANTHROPIC_API_KEY를 서버 환경 변수로 안전하게 주입해야 한다.

---

## 옵션 비교

### A. oracle 서버 자체 호스팅 (권장)

| 항목 | 내용 |
|------|------|
| 인프라 | oracle.shdkej.com (기존 서버, 추가 비용 없음) |
| 배포 방식 | git clone → pnpm install → pnpm build → PM2 |
| Nginx | 기존 설정에 server block 1개 추가 |
| 도메인 | `virtue.oracle.shdkej.com` DNS A 레코드 추가 |
| TLS | 기존 Let's Encrypt wildcard 또는 `certbot` 신규 발급 |
| API Key | `/etc/environment` 또는 PM2 ecosystem.config.js에서 주입 |
| 프라이버시 | ✅ 완전 자체 제어 |
| CD | 수동 pull + pm2 restart (초기), 또는 GitHub webhook → 자동 배포 |
| 오프라인 내성 | oracle 서버 다운 시 서비스 중단 |

**배포 스크립트 예시 (oracle 서버에서 실행):**
```bash
# 처음 한 번
cd /home/ubuntu/dev
git remote add origin https://github.com/shdkej/virtue-rebirth-app.git  # 또는 다른 레포
git push -u origin main

# oracle 서버
cd /srv/virtue-rebirth-app   # 또는 원하는 경로
git clone <repo_url> .
pnpm install --frozen-lockfile
pnpm build

# PM2 등록
pm2 start npm --name "virtue" -- start -- -p 3100
pm2 save
```

**Nginx server block (`/etc/nginx/sites-available/virtue`):**
```nginx
server {
    server_name virtue.oracle.shdkej.com;

    location / {
        proxy_pass http://localhost:3100;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
ln -s /etc/nginx/sites-available/virtue /etc/nginx/sites-enabled/
certbot --nginx -d virtue.oracle.shdkej.com
nginx -t && systemctl reload nginx
```

**환경 변수 (PM2 ecosystem):**
```js
// ecosystem.config.js
module.exports = {
  apps: [{
    name: "virtue",
    script: "node_modules/.bin/next",
    args: "start -p 3100",
    env: {
      NODE_ENV: "production",
      ANTHROPIC_API_KEY: "sk-ant-...",
      // Supabase 사용 시 추가:
      // NEXT_PUBLIC_SUPABASE_URL: "...",
      // NEXT_PUBLIC_SUPABASE_ANON_KEY: "...",
    }
  }]
};
```

---

### B. Vercel

| 항목 | 내용 |
|------|------|
| 설정 | GitHub 연동 후 자동 CI/CD |
| 비용 | 무료 (Hobby plan, 개인 프로젝트) |
| API Key | Vercel 환경 변수 대시보드에서 설정 |
| 커스텀 도메인 | Vercel DNS 또는 CNAME 레코드로 `virtue.oracle.shdkej.com` 연결 |
| serverless | API route는 Edge Function 또는 Serverless Function으로 실행 |
| 이미지 | Next.js Image Optimization 자동 제공 |
| 단점 | API 응답 Cold Start (~200ms 첫 호출), 함수 실행 시간 제한 (기본 10s) |

> Vercel은 GitHub 레포 공개 여부와 무관하게 배포 가능 (private 레포도 Hobby에서 지원).

---

### C. 로컬 Tailscale (개발용, 배포 아님)

| 항목 | 내용 |
|------|------|
| 용도 | 개인 기기에서만 접근 가능한 개발 환경 |
| 설정 | `pnpm start` + Tailscale MagicDNS |
| 단점 | 외부 접근 불가, 기기 켜져 있어야 함 |

---

## 권장 경로

```
1단계 (지금): 로컬 MVP 검증 완료 (typecheck/lint/build 통과)
2단계 (배포 전): GitHub 레포 생성 + 첫 push (사용자 컨펌 후, L1)
3단계 (배포): oracle 서버에 git clone + PM2 + Nginx 설정
4단계 (도메인): virtue.oracle.shdkej.com DNS 추가 + TLS
```

---

## 사전 체크리스트

- [ ] GitHub 레포 생성 (`virtue-rebirth-app` 또는 `shdkej/virtue-rebirth-app`)
- [ ] `.gitignore`에 `.env.local` 포함 확인 (API 키 노출 방지)
- [ ] oracle 서버에 Node 20+ 및 pnpm 설치 확인
- [ ] oracle 서버 포트 3100 (또는 다른 여유 포트) 확인
- [ ] DNS: `virtue.oracle.shdkej.com` A 레코드 또는 CNAME
- [ ] ANTHROPIC_API_KEY 서버 환경 변수 설정
- [ ] Supabase URL/KEY (영속화 구현 후)

---

## 배포 준비 순서 (로컬 Claude Code 위임용)

```
Infinity Intent: product-01 · GitHub 레포 origin 설정 + 첫 push
Mode: execute_local (사용자 컨펌 후)
Required workflow: workflow-master 먼저
Goal: /home/ubuntu/dev/virtue-rebirth-app에 GitHub origin 추가 및 첫 push

Context:
- 로컬 git: 2 commits (45a5cf3 스캐폴드, 6ba58a8 MVP 디벨롭)
- .gitignore: .env.local 반드시 포함
- 레포 이름: 사용자 결정 필요

Steps:
1. .gitignore에 .env.local 포함 확인
2. gh repo create 또는 GitHub에서 수동 생성 후 URL 획득
3. git remote add origin <url>
4. git push -u origin main

Allowed: L1 (레포 push는 사용자 컨펌 후 L2 → 이 작업은 사용자 승인 필요)
Forbidden: force push, 민감 파일 포함
Report back to: infinity/reports/product-01/{timestamp}.md
```

> **주의**: GitHub 레포 push는 L2(외부 서비스) 범주. 사용자가 GATES.md 또는 Telegram으로 승인 후 진행.
