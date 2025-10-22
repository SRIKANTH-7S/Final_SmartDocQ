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
  
  // Step 4: Verify client build is in the correct location
  console.log('📋 Verifying client build location...');
  const serverDistPath = path.join(__dirname, 'server', 'dist', 'public');
  
  if (!fs.existsSync(serverDistPath)) {
    console.error(`❌ Client build not found at: ${serverDistPath}`);
    console.log('📁 Checking if client built to different location...');
    
    // Check if it built to the old location
    const oldClientDistPath = path.join(__dirname, 'client', 'dist');
    if (fs.existsSync(oldClientDistPath)) {
      console.log('📋 Found client build in old location, copying...');
      fs.cpSync(oldClientDistPath, serverDistPath, { recursive: true });
      console.log('✅ Client build copied to correct location');
    } else {
      throw new Error(`Client build not found at expected locations`);
    }
  } else {
    console.log('✅ Client build found at:', serverDistPath);
  }
  
  console.log('✅ Build completed successfully!');
  console.log('📁 Client files copied to: server/dist/public');
  console.log('🚀 Ready for deployment!');
  
} catch (error) {
  console.error('❌ Build failed:', error.message);
  process.exit(1);
}
