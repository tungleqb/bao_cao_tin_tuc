import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import fs from 'fs'                     // ✅ THÊM DÒNG NÀY

export default defineConfig({
  plugins: [react()]
})
