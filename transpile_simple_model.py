from joblib import load

def main():
    
    model = load("model.joblib")
    coefs_c = f"static float coefs[{len(model.coef_)}] = {model.coef_};"
    
    coefs_c = coefs_c.replace('= [','= {')
    coefs_c = coefs_c.replace('];','};')
    intercept = f"{model.intercept_}"
    prediction_fonction = '\n\
    float prediction(float* features, int n_feature)\n\
    {\n\
        ' + coefs_c + '\n\
        float sum = 0;\n\
        for(int i = 0; i < n_feature; i++)\n\
            sum += coefs[i]' + '* *(features + i);\n\
        return sum + ' + intercept + ';\n\
    }\n\
    '

    main_fonction = '\n\
    int main()\n\
    {\n\
        static float X[3][1] = { {1.0}, {2.0}, {3.0} };\n\
        static float y[3] = {1.0, 4.0, 6.0};\n\
        for(int i = 0; i < 3; i++)\n\
        {\n\
            printf("%f = %f ?", y[i], prediction(X[i], 1));\n\
        }\n\
        return 0;\n\
    }\n\
    '
    with open("./transpiledCode.c", "w") as f:
        f.write("#include <stdio.h>")
        f.write(prediction_fonction)
        f.write(main_fonction)
        
if __name__ == "__main__":
    main()
