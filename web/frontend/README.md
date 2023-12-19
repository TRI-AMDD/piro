# DNA Example Web App UI

<!-- TOC -->
- [DNA Example Web App UI](#dna-example-web-app-ui)
  - [What is inside?](#what-is-inside)
  - [Getting Started](#getting-started)
    - [Install](#install)
    - [Local Run](#local-run)
    - [Lint](#lint)
    - [Typecheck](#typecheck)
    - [Build](#build)
    - [Test](#test)
  - [User Management with AWS Cognito](#user-management-with-aws-cognito)
  - [License](#license)
<!-- TOC -->

This is a boilerplate build with Vite, React 18, TypeScript, Vitest, Testing
Library, TailwindCSS 3, Eslint and Prettier.

## What is inside?

This project uses many tools like:

- [Vite](https://vitejs.dev)
- [ReactJS](https://reactjs.org)
- [TypeScript](https://www.typescriptlang.org)
- [Vitest](https://vitest.dev)
- [Testing Library](https://testing-library.com)
- [Tailwindcss](https://tailwindcss.com)
- [Eslint](https://eslint.org)
- [Prettier](https://prettier.io)
- [React Router](https://reactrouter.com)
- [TanStack Query](https://tanstack.com/query/latest/docs/react/overview)

## Getting Started

### Install

Install dependencies.

```bash
pnpm install
```

### Local Run

Serve with hot reload at <http://localhost:3000>.

```bash
pnpm run dev
```

Or with Docker

```bash
docker compose build && docker compose watch
```

### Lint

```bash
pnpm run lint
```

### Typecheck

```bash
pnpm run typecheck
```

### Build

```bash
pnpm run build
```

Or with Docker

```bash
docker build -t export-prod -o dist .
```

### Test

```bash
pnpm run test
```

View and interact with your tests via UI.

```bash
pnpm run test:ui
```

## User Management with AWS Cognito

The app supports AWS Cognito login using Cognito's hosted UI. To enable
Cognito, supply the details in the [config.js](public/config.js) to connect to
the desired Cognito user pool and set the flag `AMPLIFY_ENABLED` to true.

## License

This project is licensed under the MIT License.
