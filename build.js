import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log('🏗️  Starting build process...');

try {
  // Step 1: Install client dependencies and build
  console.log('📦 Installing client dependencies...');
  execSync('npm install', { cwd: path.join(__dirname, 'client'), stdio: 'inherit' });
  
  console.log('🔨 Building client...');
  execSync('npm run build', { cwd: path.join(__dirname, 'client'), stdio: 'inherit' });
  
  // Step 2: Install server dependencies
  console.log('📦 Installing server dependencies...');
  execSync('npm install', { cwd: path.join(__dirname, 'server'), stdio: 'inherit' });
  
  // Step 3: Build server
  console.log('🔨 Building server...');
  execSync('npm run build:server', { cwd: path.join(__dirname, 'server'), stdio: 'inherit' });
  
  // Step 4: Copy client build to server dist
  console.log('📋 Copying client build to server dist...');
  const clientDistPath = path.join(__dirname, 'client', 'dist');
  const serverDistPath = path.join(__dirname, 'server', 'dist', 'public');
  
  if (fs.existsSync(serverDistPath)) {
    fs.rmSync(serverDistPath, { recursive: true });
  }
  
  fs.cpSync(clientDistPath, serverDistPath, { recursive: true });
  
  console.log('✅ Build completed successfully!');
  console.log('📁 Client files copied to: server/dist/public');
  console.log('🚀 Ready for deployment!');
  
} catch (error) {
  console.error('❌ Build failed:', error.message);
  process.exit(1);
}
