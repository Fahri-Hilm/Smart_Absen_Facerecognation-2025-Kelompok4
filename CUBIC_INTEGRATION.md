# Integrasi cubic.dev AI Code Reviewer

## Setup

1. Buka https://cubic.dev/sign-up
2. Login dengan GitHub account
3. Install cubic GitHub App ke repository ini
4. cubic akan otomatis review setiap pull request

## Cara Menggunakan

### Review Otomatis
- Setiap PR baru akan otomatis direview oleh cubic AI
- cubic akan memberikan komentar untuk bug, improvement, dan best practices

### Review Manual
Untuk PR yang sudah ada sebelum install cubic:
```
@cubic-dev-ai review this PR
```

### Minta Fix Otomatis
```
@cubic-dev-ai fix this issue
```

### Tanya AI
```
@cubic-dev-ai apakah kode ini aman untuk data biometrik?
@cubic-dev-ai bagaimana cara optimize face recognition ini?
```

## Konfigurasi

File `cubic.yaml` sudah dikonfigurasi dengan:
- Custom rules untuk security face recognition
- Custom rules untuk database security
- Custom rules untuk Flask authentication
- Ignore patterns untuk file binary dan model
