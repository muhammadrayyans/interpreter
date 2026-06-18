echo "🧹 Wiping the Cython cache completely..."

cd modules

rm -rf build
cd ..

cd config

rm -f *.c
rm -f *.so
rm -f *.pyd
cd ..


cd io_tree

rm -f *.c
rm -f *.so
rm -f *.pyd
cd ..

cd modules

rm -rf __pycache__

echo "⚙️  Compiling Cython extension freshly..."
python setup.py build_ext --inplace

cd ..

echo "🚀 Running Python application..."
echo ""
echo "--------------------------------"
echo ""
python main.py