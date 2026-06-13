echo "🧹 Cleaning up old build files..."

cd modules

rm -r  build

echo "⚙️  Compiling Cython extension..."
python setup.py build_ext --inplace

cd ..

echo "🚀 Running Python application..."
echo ""
echo "--------------------------------"
echo ""
python main.py
