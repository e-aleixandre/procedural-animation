enum FlowType
{
    RANDOM, PERLIN, CENTER
}

class FlowField
{
    PVector[][] field;
    int cols, rows;
    int resolution;

    FlowField(FlowType type, int r) {
        resolution = r;
        cols = width / resolution;
        rows = height / resolution;
        field = new PVector[cols][rows];
        init(type);
    }

    void draw() {
        for (int i = 0; i < cols; i++)
        {
            for (int j = 0; j < rows; j++)
            {
                PVector cellCenter = new PVector(i * resolution + resolution / 2, j * resolution + resolution / 2);
                drawVector(cellCenter, field[i][j]);
            }
        }
    }

    PVector lookup(PVector position) {
        int column = constrain(int(position.x / resolution), 0, cols - 1);
        int row = constrain(int(position.y / resolution), 0, rows - 1);
        
        return field[column][row].copy();
    }

    private void init(FlowType type) {
        switch (type) {
            case CENTER:
                centerFlowField();
                break;
            case RANDOM:
                randomFlowField();
                break;
            case PERLIN:
            default:
                perlinFlowField();
        }
    }

    private void centerFlowField() {
        PVector screenCenter = new PVector(width / 2, height / 2);
        
        for (int i = 0; i < cols; i++) {
            for (int j = 0; j < rows; j++) {
                PVector cellCenter = new PVector(i * resolution + resolution / 2, j * resolution + resolution / 2);
                PVector vector = PVector.sub(screenCenter, cellCenter);
                vector.normalize();
                field[i][j] = vector;
            }
        }
    }

    private void randomFlowField() {
        for (int i = 0; i < cols; i++) {
            for (int j = 0; j < rows; j++) {
                field[i][j] = PVector.random2D();
            }
        }
    }

    private void perlinFlowField() {
        float xoff = 0;
        for (int i = 0; i < cols; i++) {
            float yoff = 0;
            for (int j = 0; j < rows; j++) {
                float theta = map(noise(xoff, yoff), 0, 1, 0, TWO_PI);
                field[i][j] = new PVector(cos(theta), sin(theta));
                yoff += 0.2;
            }
            xoff += 0.2;
        }
    }

    private void drawVector(PVector center, PVector vector) {
        pushMatrix();
        {
            stroke(255, 255, 255);
            fill(255, 255, 255);
            
            translate(center.x, center.y);
            rotate(atan2(vector.y, vector.x));
            line(0, 0, vector.mag() + resolution / 4, 0);
            line(vector.mag() + resolution / 4, 0, vector.mag() + resolution / 4 - resolution / 8, - resolution / 8);
            line(vector.mag() + resolution / 4, 0, vector.mag() + resolution / 4 - resolution / 8, resolution / 8);
        }
        popMatrix();
    }
}