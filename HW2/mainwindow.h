#ifndef MAINWINDOW_H
#define MAINWINDOW_H

# include <QMainWindow>
# include <QFileDialog>
# include <QtCharts>
# include <QtCharts/QChartView>
# include <QtCharts/QBarSeries>
# include <QtCharts/QBarSet>
# include <QtCharts/QLegend>
# include <QtCharts/QBarCategoryAxis>

# include <iostream>
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
    Mat MatImgIn;
    QImage QimgIn, QimgOut;
    QString hisTitle;
    int pixelCount[256], imgCols, imgRows, *imgOutPixel;
    double equalizationTable[256];

    void showOutput(int *pixelCount, QString title);
    int checkPixel(int pixel);
    Mat QImage2Mat(const QImage& src);

private slots:
    void on_openImg_clicked();
    void on_grayAImg_clicked();
    void on_grayBImg_clicked();
    void on_compare_clicked();
    void on_autoContrastImg_clicked();
    void on_enlarge_clicked();
    void on_brightnessImg_clicked();
    void on_thresholdImg_clicked();
    void on_contrastImg_clicked();
    void on_quit_clicked();
};

#endif // MAINWINDOW_H
