/// <reference types="vitest" />
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';
import tsconfigPaths from 'vite-tsconfig-paths';
import path from 'path';

// https://vitejs.dev/config https://vitest.dev/config
export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  test: {
    globals: true,
    environment: 'happy-dom',
    setupFiles: '.vitest/setup',
    include: ['**/test.{ts,tsx}']
  },
  // https://github.com/vitejs/vite/issues/1973
  // define: {
  //   // "process.env": process.env,
  //   // By default, Vite doesn't include shims for NodeJS/
  //   // necessary for amplify lib to work
  //   global: {}
  // },
  resolve: {
    alias: [
      {
        find: './runtimeConfig',
        replacement: './runtimeConfig.browser' // ensures browser compatible version of AWS JS SDK is used
      },
      {
        find: '@',
        replacement: path.resolve(__dirname, 'src')
      }
    ]
  },
  server: {
      port: 3000,
      proxy: {
        '/api': 'http://127.0.0.1:80'
    }
  }
});
