#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    this->setWindowTitle("Image Viewer");
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_openImg_clicked()
{
    // Open Image
    QString filePath = QFileDialog::getOpenFileName(this, tr("Open Image"), ".", tr("Images(*.bmp *.jpeg *.png *.jpg)"));
    MatImgIn = imread(filePath.toStdString());
    if (!MatImgIn.empty())
    {
        cvtColor(MatImgIn, MatImgIn, COLOR_BGR2RGB);
        QimgIn = QImage((const unsigned char*) (MatImgIn.data), MatImgIn.cols, MatImgIn.rows, QImage::Format_RGB888);
        // Show Image
        ui->showimgIn->setPixmap(QPixmap::fromImage(QimgIn.scaled(ui->showimgIn->width(),ui->showimgIn->height(),Qt::KeepAspectRatio)));
    }
    // Set up variables
    imgCols = MatImgIn.cols;
    imgRows = MatImgIn.rows;
    imgOutPixel = new int[imgCols*imgRows];
    QimgOut = QImage(imgCols, imgRows, QImage::Format_RGB32);
    for (int i = 0 ; i < 256 ; i++)
        pixelCount[i] = 0;

    // Count the pixel
    int index = 0;
    for (int i = 0 ; i < imgCols ; i++)
    {
        for (int j = 0 ; j < imgRows ; j++)
        {
            double B = MatImgIn.at<Vec3b>(j,i)[0], G = MatImgIn.at<Vec3b>(j,i)[1], R = MatImgIn.at<Vec3b>(j,i)[2];  // Get pixels
            double pixel = 0.299*R + 0.587*G + 0.114*B;                        // Do grayscale
            QimgOut.setPixel(i, j, qRgb(int(pixel), int(pixel), int(pixel)));  // Set grayscale from double to int

            // Count the pixel
            pixelCount[int(pixel)] += 1;

            // Put pixel in 1-D array
            imgOutPixel[index] = int(pixel);
            index += 1;
        }
    }

    hisTitle = "Grayscale Histogram";
    showOutput(pixelCount, hisTitle);
}



void MainWindow::on_grayAImg_clicked()
{
    // Set up variable
    for (int i = 0 ; i < 256 ; i++)
        pixelCount[i] = 0;

    // Count the pixel
    int index = 0;
    for (int i = 0 ; i < imgCols ; i++)
    {
        for (int j = 0 ; j < imgRows ; j++)
        {
            double B = MatImgIn.at<Vec3b>(j,i)[0], G = MatImgIn.at<Vec3b>(j,i)[1], R = MatImgIn.at<Vec3b>(j,i)[2];  // Get pixels
            double pixel = 0.333*B + 0.333*G + 0.333*R;                        // Do grayscale
            QimgOut.setPixel(i, j, qRgb(int(pixel), int(pixel), int(pixel)));  // Set grayscale from double to int

            // Count the pixel
            pixelCount[int(pixel)] += 1;

            // Put pixel in 1-D array
            imgOutPixel[index] = int(pixel);
            index += 1;
        }
    }

    hisTitle = "Grayscale A Histogram";
    showOutput(pixelCount, hisTitle);
}

void MainWindow::on_grayBImg_clicked()
{
    // Set up variable
    for (int i = 0 ; i < 256 ; i++)
        pixelCount[i] = 0;

    // Count the pixel
    int index = 0;
    for (int i = 0 ; i < imgCols ; i++)
    {
        for (int j = 0 ; j < imgRows ; j++)
        {
            double B = MatImgIn.at<Vec3b>(j,i)[0], G = MatImgIn.at<Vec3b>(j,i)[1], R = MatImgIn.at<Vec3b>(j,i)[2];  // Get pixels
            double pixel = 0.299*R + 0.587*G + 0.114*B;                        // Do grayscale
            QimgOut.setPixel(i, j, qRgb(int(pixel), int(pixel), int(pixel)));  // Set grayscale from double to int

            // Count the pixel
            pixelCount[int(pixel)] += 1;

            // Put pixel in 1-D array
            imgOutPixel[index] = int(pixel);
            index += 1;
        }
    }

    hisTitle = "Grayscale B Histogram";
    showOutput(pixelCount, hisTitle);
}


void MainWindow::on_compare_clicked()
{
    // Set up variable
    for (int i = 0 ; i < 256 ; i++)
        pixelCount[i] = 0;

    // Count the pixel
    int index = 0;
    for (int i = 0 ; i < imgCols ; i++)
    {
        for (int j = 0 ; j < imgRows ; j++)
        {
            double B = MatImgIn.at<Vec3b>(j,i)[0], G = MatImgIn.at<Vec3b>(j,i)[1], R = MatImgIn.at<Vec3b>(j,i)[2];
            double pixelA = 0.333*B + 0.333*G + 0.333*R;
            double pixelB = 0.299*R + 0.587*G + 0.114*B;
            int pixel = int(pixelB-pixelA);

            // Put pixel in 1-D array
            imgOutPixel[index] = pixel;
            index += 1;

            // Put pixel in QimgOut
            pixel = checkPixel(pixel);
            QimgOut.setPixel(i, j, qRgb(pixel, pixel, pixel));

            // Count the pixel
            pixelCount[int(pixel)] += 1;
        }
    }

    hisTitle = " Difference histogram from two methods";
    showOutput(pixelCount, hisTitle);
}

void MainWindow::on_autoContrastImg_clicked()
{
    // Get equalizationTable
    int cdf = 0;
    for (int i = 0 ; i < 256 ; i++)
    {
        cdf +=  pixelCount[i];
        equalizationTable[i] = cdf;
    }
    double minCDF = equalizationTable[0], maxCDF = equalizationTable[255];
    for (int i = 0 ; i < 256 ; i++)
    {
        equalizationTable[i] = (equalizationTable[i]-minCDF)/(maxCDF - minCDF)*255;
        pixelCount[i] = 0;
    }

    // Count the pixel
    int index = 0;
    for (int i = 0 ; i < imgCols ; i++)
    {
        for (int j = 0 ; j < imgRows ; j++)
        {
            int pixel = int(equalizationTable[checkPixel(imgOutPixel[index])]);  // Key Point
            imgOutPixel[index] = pixel;
            index ++;

            pixel = checkPixel(pixel);
            QimgOut.setPixel(i, j, qRgb(pixel, pixel, pixel));
            pixelCount[pixel] += 1;
        }
    }

    hisTitle = "Histogram Equalization";
    showOutput(pixelCount, hisTitle);
}

void MainWindow::on_enlarge_clicked()
{
    // Set up variables
    QImage QimgEnlarge = QImage(imgCols*2, imgRows*2, QImage::Format_RGB32);

    // Set pixel to 2x pixel
    int index = 0;
    for (int i = 0 ; i < imgCols*2 ; i+=2)
    {
        for (int j = 0 ; j < imgRows*2 ; j+=2)
        {
            // Set pixel
            int pixel = imgOutPixel[index];
            pixel = checkPixel(pixel);
            QimgEnlarge.setPixel(i, j, qRgb(pixel, pixel, pixel));
            QimgEnlarge.setPixel(i+1, j, qRgb(pixel, pixel, pixel));
            QimgEnlarge.setPixel(i, j+1, qRgb(pixel, pixel, pixel));
            QimgEnlarge.setPixel(i+1, j+1, qRgb(pixel, pixel, pixel));
            index ++;
        }
    }

    // Convert QImage to Mat
    Mat MatEnlarge = QImage2Mat(QimgEnlarge);
    Mat MatOrigine = QImage2Mat(QimgOut);

    // Show 2x Image
    //imshow("Original Image", MatOrigine); //Show original image
    imshow("Zoom in 2X Image", MatEnlarge); //Show 2x image
    waitKey(0);
    destroyAllWindows();
}

void MainWindow::on_brightnessImg_clicked()
{
    // Set up variables
    int brightness = ui->brightness->text().toInt();
    for (int i = 0 ; i < 256 ; i++)
        pixelCount[i] = 0;

    // Count the pixel
    int index = 0;
    for (int i = 0 ; i < imgCols ; i++)
    {
        for (int j = 0 ; j < imgRows ; j++)
        {
            // Do brightness
            int pixel = imgOutPixel[index];
            pixel += brightness;

            imgOutPixel[index] = pixel;
            index ++;

            pixel = checkPixel(pixel);
            QimgOut.setPixel(i, j, qRgb(pixel, pixel, pixel));

            // Count histogram
            pixelCount[pixel] += 1;
        }
    }

    showOutput(pixelCount, hisTitle);
}

void MainWindow::on_thresholdImg_clicked()
{
    // Set up variables
    int threshold = ui->threshold->text().toInt();
    for (int i = 0 ; i < 256 ; i++)
        pixelCount[i] = 0;

    // Count the pixel
    int index = 0;
    for (int i = 0 ; i < imgCols ; i++)
    {
        for (int j = 0 ; j < imgRows ; j++)
        {
            // Do threshold
            int pixel = imgOutPixel[index];
            if (pixel >= threshold)
            {
                QimgOut.setPixel(i, j, qRgb(255, 255, 255));
                pixelCount[255] += 1;
                imgOutPixel[index] = 255;
            }
            else
            {
                QimgOut.setPixel(i, j, qRgb(0, 0, 0));
                pixelCount[0] += 1;
                imgOutPixel[index] = 0;
            }
            index ++;
        }
    }

    hisTitle = "Manual Threshold Histogram";
    showOutput(pixelCount, hisTitle);
}

void MainWindow::on_contrastImg_clicked()
{
    // Set up variables
    double contrast = ui->contrast->text().toDouble();
    for (int i = 0 ; i < 256 ; i++)
        pixelCount[i] = 0;

    // Count the pixel
    int index = 0;
    for (int i = 0 ; i < imgCols ; i++)
    {
        for (int j = 0 ; j < imgRows ; j++)
        {
            // Do contrast
            int pixel = imgOutPixel[index];
            pixel *= contrast;

            imgOutPixel[index] = pixel;
            index ++;

            pixel = checkPixel(pixel);
            QimgOut.setPixel(i, j, qRgb(pixel, pixel, pixel));

            // Count histogram
            pixelCount[pixel] += 1;
        }
    }

    showOutput(pixelCount, hisTitle);
}

void MainWindow::showOutput(int *pixelCount, QString title)
{
    ui->showimgOut->setPixmap(QPixmap::fromImage(QimgOut.scaled(ui->showimgOut->width(),ui->showimgOut->height(),Qt::KeepAspectRatio)));

    QBarSet *set = new QBarSet(title);
    int yMax = 0;
    for (int i = 0 ; i < 256 ; i++)
    {
        set->append(pixelCount[i]);
        if(yMax < pixelCount[i])
            yMax = pixelCount[i];
        set->setColor(QColor::Rgb);
    }

    QValueAxis *axisY = new QValueAxis;
    axisY->setLabelFormat("%d");
    axisY->setRange(0,yMax);

    QBarSeries *series = new QBarSeries();
    series->append(set);
    series->setBarWidth(1);

    QChart *chart = new QChart();
    chart->addSeries(series);
    chart->createDefaultAxes();
    QFont font;
    font.setPixelSize(18);
    chart->setTitleFont(font);
    chart->setTitle(title);
    chart->setAnimationOptions(QChart::SeriesAnimations);
    chart->legend()->setVisible(false);

    ui->showHis->setChart(chart);
}

int MainWindow::checkPixel(int pixel)
{
    if (pixel > 255)
        pixel = 255;
    else if (pixel < 0)
        pixel = 0;
    return pixel;
}

Mat MainWindow::QImage2Mat(const QImage& src)
{
    Mat mat = Mat(src.height(), src.width(), CV_8UC4, (uchar*)src.bits(), src.bytesPerLine());
    Mat result = Mat(mat.rows, mat.cols, CV_8UC3 );
    int from_to[] = { 0,0,  1,1,  2,2 };
    mixChannels( &mat, 1, &result, 1, from_to, 3 );
    return result;
}

void MainWindow::on_quit_clicked()
{
    QApplication::quit();
}
