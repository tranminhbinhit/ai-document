#!/bin/bash

# Script to setup Angular frontend structure

cd frontend

# Create directory structure
mkdir -p src/app/{models,services,pages/{chat,upload,documents},components}

# Create environment file
cat > src/environments/environment.ts << 'EOF'
export const environment = {
  production: false,
  apiUrl: 'http://localhost:5000/api'
};
EOF

cat > src/environments/environment.prod.ts << 'EOF'
export const environment = {
  production: true,
  apiUrl: '/api'
};
EOF

echo "Frontend structure created. Run: cd frontend && npm install"
