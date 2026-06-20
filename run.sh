echo "🧹 Wiping the Cython cache completely..."

cd src/modules

rm -rf build
cd ../..

cd src/config

rm -f *.c
rm -f *.so
rm -f *.pyd
cd ../..


cd src/io_tree

rm -f *.c
rm -f *.so
rm -f *.pyd
cd ../..

cd src/parser

rm -f *.c
rm -f *.so
rm -f *.pyd
cd ../..

cd src/library

rm -f *.c
rm -f *.so
rm -f *.pyd
cd ../..

cd src/data_node

rm -f *.c
rm -f *.so
rm -f *.pyd
cd ../..


cd src/condition_tree

rm -f *.c
rm -f *.so
rm -f *.pyd
cd ../..

cd src/modules


rm -rf __pycache__

echo "⚙️  Compiling Cython extension freshly..."
python setup.py build_ext --inplace

cd ../..

echo "🚀 Running Python application..."
echo ""
echo "--------------------------------"
echo ""
python src/main.py