for file in $(find -not -path "./.*" -not -path "./docs*" \( -name "*.py" -o -name "*.toml" \) ); do
    sed -i -e "s/0.0.0+auto.0/9.0.1/" $file;
done;
