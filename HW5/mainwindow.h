#ifndef MAINWINDOW_H
#define MAINWINDOW_H

# include <QMainWindow>
# include <QFileDialog>
# include <QColorDialog>
# include <iostream>
# include <math.h>
# include <random>
using namespace std;

# include <opencv2/highgui/highgui.hpp>
# include <opencv2/core/types.hpp>
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
    Mat MatImgIn, kmeansData, kmeansResult, label, center;
    QImage QImgIn, QImgOut, QImgBarGray, QImgBarRGB;
    QString colorData01, colorData02;

    int imgCols, imgRows, pseudoColorTable[256][3];

    double checkPixel(double pixel);
    double LAB_hq_func(double q);
    void showColorBar();

private slots:

    void on_actionOpen_triggered();
    void on_RGB_clicked();
    void on_CMY_clicked();
    void on_actionClose_triggered();
    void on_HSI_clicked();
    void on_XYZ_clicked();
    void on_LAB_clicked();
    void on_YUV_clicked();
    void on_pseudoColor_clicked();
    void on_changeColor_clicked();
    void on_kMeans_clicked();
};

#endif // MAINWINDOW_H
