#!/bin/bash

echo "🚀 CredHand Backend Setup Script"
echo "=================================="
echo ""

# Step 1: Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Step 2: Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Step 3: Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 4: Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Step 5: Load sample data
echo "📊 Loading sample credit cards..."
python manage.py loaddata cards/fixtures/sample_cards.json 2>/dev/null || echo "⚠️  Sample data already loaded or not available"

# Step 6: Create superuser prompt
echo ""
echo "👤 Creating superuser account..."
python manage.py createsuperuser

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "   1. Update .env file with your credentials"
echo "   2. Run: python manage.py runserver"
echo "   3. Visit: http://localhost:8000/"
echo ""
