#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

# include <QMainWindow>
# include <QFileDialog>
# include <iostream>
# include <algorithm>
# include <sstream>
# include <cstdlib>
# include <string>
# include <math.h>
# define PI acos(-1)
using namespace std;

# include <opencv2/highgui/highgui.hpp>
# include <opencv2/core/core.hpp>
# include <opencv2/imgproc.hpp>
using namespace cv;

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private:
    Ui::MainWindow *ui;

    int imgCols, imgRows, maskSize, orderMaskSize, pixelB, pixelG, pixelR, pixel;
    double BGRCoefficient, sigma;

    String coefficientsString, splitResult;
    Mat MatImgIn, MatForZero;
    QImage QImgIn, QImgOut;
    vector<int> pixelSeriesB, pixelSeriesG, pixelSeriesR;
    vector<double> coefficientsDouble;

    int pixelCheck(int index);

private slots:
    void on_actionopen_triggered();
    void on_actionclose_triggered();
    void on_convImg_clicked();
    void on_LoGImg_clicked();
    void on_gaussianImg_clicked();
    void on_local_enhancement_clicked();
    void on_local_enhancement_2_clicked();
};

#endif // MAINWINDOW_H
