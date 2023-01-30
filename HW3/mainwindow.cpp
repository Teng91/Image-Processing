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

void MainWindow::on_actionopen_triggered()
{
    // Open Image
    QString filePath = QFileDialog::getOpenFileName(this, tr("Open Image"), ".", tr("Images(*.bmp *.jpeg *.png *.jpg)"));
    MatImgIn = imread(filePath.toStdString());
    if (!MatImgIn.empty())
    {
        imgCols = MatImgIn.cols;
        imgRows = MatImgIn.rows;
        // Set Image
        QImgIn = QImage(imgCols, imgRows, QImage::Format_RGB32);
        for (int i = 0 ; i < imgCols ; i++)
        {
            for (int j = 0 ; j < imgRows ; j++)
            {
                int B = MatImgIn.at<Vec3b>(j,i)[0], G = MatImgIn.at<Vec3b>(j,i)[1], R = MatImgIn.at<Vec3b>(j,i)[2];
                QImgIn.setPixel(i, j, qRgb(R, G, B));
            }
        }
        // Show Image
        ui->showImgIn->setPixmap(QPixmap::fromImage(QImgIn.scaled(ui->showImgIn->width(),ui->showImgIn->height(),Qt::KeepAspectRatio)));
    }
}

void MainWindow::on_actionclose_triggered()
{
    QApplication::quit();
}

void MainWindow::on_convImg_clicked()
{
    // Set up variables
    maskSize = ui->maskSize->text().toInt();
    QImgOut = QImage(imgCols-maskSize+1, imgRows-maskSize+1, QImage::Format_RGB32);
    int index;
    // Set mask size
    coefficientsString = ui->maskCoefficients->text().toStdString();
    stringstream input(coefficientsString);
    coefficientsDouble.clear();
    // Split mask size coefficients String by space and transform it to double
    while(input>>splitResult)
        coefficientsDouble.push_back(atof(splitResult.c_str()));
    // find the central element of a mask
    for (int i = (maskSize+1)/2-1 ; i < imgCols-(maskSize-1)/2 ; i++)
    {
        for (int j = (maskSize+1)/2-1 ; j < imgRows-(maskSize-1)/2 ; j++)
        {
            // Regulate the variables
            pixelB = 0;
            pixelG = 0;
            pixelR = 0;
            index = maskSize*maskSize - 1;
            // insert the mask elements in vector and do the convolution
            for (int x = i-(maskSize-1)/2 ; x < i-(maskSize-1)/2+maskSize ; x++)
            {
                for (int y = j-(maskSize-1)/2 ; y < j-(maskSize-1)/2+maskSize ; y++)
                {
                    // Get pixels
                    double B = MatImgIn.at<Vec3b>(y,x)[0], G = MatImgIn.at<Vec3b>(y,x)[1], R = MatImgIn.at<Vec3b>(y,x)[2];
                    BGRCoefficient = coefficientsDouble.at(index);
                    // pixels multiply Coefficient
                    pixelB += (B * BGRCoefficient);
                    pixelG += (G * BGRCoefficient);
                    pixelR += (R * BGRCoefficient);
                    index --;
                }
            }
            // Check pixel
            pixelB = pixelCheck(pixelB);
            pixelG = pixelCheck(pixelG);
            pixelR = pixelCheck(pixelR);
            // Set pixel
            QImgOut.setPixel(i-(maskSize+1)/2+1, j-(maskSize+1)/2+1, qRgb(pixelR, pixelG, pixelB));
        }
    }
    // Show Image
    ui->showImgOut->setPixmap(QPixmap::fromImage(QImgOut.scaled(ui->showImgOut->width(),ui->showImgOut->height(),Qt::KeepAspectRatio)));
}

void MainWindow::on_LoGImg_clicked()
{
    // Set up variables
    maskSize = 3;
    QImgOut = QImage(imgCols-maskSize+1, imgRows-maskSize+1, QImage::Format_RGB32);
    double log3DMask[3][3] = {{-1,-1,-1},
                              {-1,8,-1},
                              {-1,-1,-1}};
    // Set mask size
    coefficientsDouble.clear();
    for (int i = 0 ; i < maskSize ; i ++)
        for (int j = 0 ; j < maskSize ; j++)
            coefficientsDouble.push_back(log3DMask[i][j]);
    int index;
    // find the central element of a mask
    for (int i = (maskSize+1)/2-1 ; i < imgCols-(maskSize-1)/2 ; i++)
    {
        for (int j = (maskSize+1)/2-1 ; j < imgRows-(maskSize-1)/2 ; j++)
        {
            // Regulate the variables
            pixelB = 0;
            pixelG = 0;
            pixelR = 0;
            index = maskSize*maskSize - 1;
            // insert the mask elements in vector and do the convolution
            for (int x = i-(maskSize-1)/2 ; x < i-(maskSize-1)/2+maskSize ; x++)
            {
                for (int y = j-(maskSize-1)/2 ; y < j-(maskSize-1)/2+maskSize ; y++)
                {
                    // Get pixels
                    double B = MatImgIn.at<Vec3b>(y,x)[0], G = MatImgIn.at<Vec3b>(y,x)[1], R = MatImgIn.at<Vec3b>(y,x)[2];
                    BGRCoefficient = coefficientsDouble.at(index);
                    // pixels multiply Coefficient
                    pixelB += (B * BGRCoefficient);
                    pixelG += (G * BGRCoefficient);
                    pixelR += (R * BGRCoefficient);
                    index --;
                }
            }
            // Check pixel
            pixelB = pixelCheck(pixelB);
            pixelG = pixelCheck(pixelG);
            pixelR = pixelCheck(pixelR);
            pixel = (pixelB + pixelG + pixelR)/3;
            // Set pixel
            QImgOut.setPixel(i-(maskSize+1)/2+1, j-(maskSize+1)/2+1, qRgb(pixel, pixel, pixel));
        }
    }
    // Show Image
    ui->showImgOut->setPixmap(QPixmap::fromImage(QImgOut.scaled(ui->showImgOut->width(),ui->showImgOut->height(),Qt::KeepAspectRatio)));
}

void MainWindow::on_gaussianImg_clicked()
{
    // Set up variables
    maskSize = 9;
    QImgOut = QImage(imgCols-maskSize+1, imgRows-maskSize+1, QImage::Format_RGB32);
    MatForZero = Mat(imgCols-maskSize+1, imgRows-maskSize+1, CV_64FC1);
    double log3DMask[9][9] = {{0, 0, 3, 2, 2, 2, 3, 0, 0},
                              {0, 2, 3, 5, 5, 5, 3, 2, 0},
                              {3, 3, 5, 3, 0, 3, 5, 3, 3},
                              {2, 5, 3, -12, -23, -12, 3, 5, 2},
                              {2, 5, 0, -23, -40, -23, 0, 5, 2},
                              {2, 5, 3, -12, -23, -12, 3, 5, 2},
                              {3, 3, 5, 3, 0, 3, 5, 3, 3},
                              {0, 2, 3, 5, 5, 5, 3, 2, 0},
                              {0, 0, 3, 2, 2, 2, 3, 0, 0}};
    // Set mask size
    coefficientsDouble.clear();
    for (int i = 0 ; i < maskSize ; i ++)
        for (int j = 0 ; j < maskSize ; j++)
            coefficientsDouble.push_back(log3DMask[i][j]);
    int index;
    // find the central element of a mask
    for (int i = (maskSize+1)/2-1 ; i < imgCols-(maskSize-1)/2 ; i++)
    {
        for (int j = (maskSize+1)/2-1 ; j < imgRows-(maskSize-1)/2 ; j++)
        {
            // Regulate the variables
            pixelB = 0;
            pixelG = 0;
            pixelR = 0;
            index = maskSize*maskSize - 1;
            // insert the mask elements in vector and do the convolution
            for (int x = i-(maskSize-1)/2 ; x < i-(maskSize-1)/2+maskSize ; x++)
            {
                for (int y = j-(maskSize-1)/2 ; y < j-(maskSize-1)/2+maskSize ; y++)
                {
                    // Get pixels
                    double B = MatImgIn.at<Vec3b>(y,x)[0], G = MatImgIn.at<Vec3b>(y,x)[1], R = MatImgIn.at<Vec3b>(y,x)[2];
                    BGRCoefficient = coefficientsDouble.at(index);
                    // pixels multiply Coefficient
                    pixelB += (B * BGRCoefficient);
                    pixelG += (G * BGRCoefficient);
                    pixelR += (R * BGRCoefficient);
                    index --;
                }
            }
            // Check pixel
            pixelB = pixelCheck(pixelB);
            pixelG = pixelCheck(pixelG);
            pixelR = pixelCheck(pixelR);
            pixel = (pixelB + pixelG + pixelR)/3;
            MatForZero.at<double>(i-(maskSize+1)/2+1, j-(maskSize+1)/2+1) = pixel;
        }
    }
    // Find zero-crossing
    for (int i = 1 ; i < imgCols-maskSize ; i++)
    {
        for (int j = 1 ; j < imgRows-maskSize ; j++)
        {
            if ((MatForZero.at<double>(i - 1, j) * MatForZero.at<double>(i + 1, j) <= 0) || (MatForZero.at<double>(i, j + 1) * MatForZero.at<double>(i, j - 1) <= 0) || (MatForZero.at<double>(i + 1, j - 1) * MatForZero.at<double>(i - 1, j + 1) <= 0) || (MatForZero.at<double>(i - 1, j - 1) * MatForZero.at <double> (i + 1, j + 1) <= 0))
                // Set pixel
                QImgOut.setPixel(i, j, qRgb(255, 255, 255));
            else
                // Set pixel
                QImgOut.setPixel(i, j, qRgb(0, 0, 0));
        }
    }
    // Show Image
    ui->showImgOut->setPixmap(QPixmap::fromImage(QImgOut.scaled(ui->showImgOut->width(),ui->showImgOut->height(),Qt::KeepAspectRatio)));
}

int MainWindow::pixelCheck(int index)
{
    if (index > 255)
        index = 255;
    else if (index < 0)
        index = 0;
    return index;
}

void MainWindow::on_local_enhancement_clicked()
{
    // Set up variables
    double k_0 = 0, k_1 = 0.25, k_2 = 0, k_3 = 0.1;
    double C= 22.8, C_1 = 0;
    int kernal_size = 1;
    QImgOut = QImage(imgCols+1, imgRows+1, QImage::Format_RGB32);
    int index;
    // find the central element of a mask
        for (int i = (kernal_size+1)/2-1 ; i < imgCols-(kernal_size-1)/2 ; i++)
        {
            for (int j = (kernal_size+1)/2-1 ; j < imgRows-(kernal_size-1)/2 ; j++)
            {
                // Regulate the variables
                pixelB = 0;
                pixelG = 0;
                pixelR = 0;
                index = kernal_size*kernal_size - 1;
                // insert the mask elements in vector and do the convolution
                for (int x = i-(kernal_size-1)/2 ; x < i-(kernal_size-1)/2+kernal_size ; x++)
                {
                    for (int y = j-(kernal_size-1)/2 ; y < j-(kernal_size-1)/2+kernal_size ; y++)
                    {
                        // Get pixels
                        double B = MatImgIn.at<Vec3b>(y,x)[0], G = MatImgIn.at<Vec3b>(y,x)[1], R = MatImgIn.at<Vec3b>(y,x)[2];
                        //BGRCoefficient = coefficientsDouble.at(index);
                        // pixels multiply Coefficient
                        pixelB += (B * C + C_1);
                        pixelG += (G * C + C_1);
                        pixelR += (R * C + C_1);
                        index --;
                    }
                }
                // Check pixel
                pixelB = pixelCheck(pixelB);
                pixelG = pixelCheck(pixelG);
                pixelR = pixelCheck(pixelR);
                // Set pixel
                QImgOut.setPixel(i-(kernal_size+1)/2+1, j-(kernal_size+1)/2+1, qRgb(pixelR, pixelG, pixelB));
            }
        }
        // Show Image
        ui->showImgOut->setPixmap(QPixmap::fromImage(QImgOut.scaled(ui->showImgOut->width(),ui->showImgOut->height(),Qt::KeepAspectRatio)));
}

void MainWindow::on_local_enhancement_2_clicked()
{
    // Set up variables
    double k_0 = 0, k_1 = 5, k_2 = 0, k_3 = 0.5;
    double C= 2.7, C_1 = 10;
    int kernal_size = 1;
    QImgOut = QImage(imgCols+1, imgRows+1, QImage::Format_RGB32);
       int index;
       // find the central element of a mask
           for (int i = (kernal_size+1)/2-1 ; i < imgCols-(kernal_size-1)/2 ; i++)
           {
               for (int j = (kernal_size+1)/2-1 ; j < imgRows-(kernal_size-1)/2 ; j++)
               {
                   // Regulate the variables
                   pixelB = 0;
                   pixelG = 0;
                   pixelR = 0;
                   index = kernal_size*kernal_size - 1;
                   // insert the kernal_size in vector and do the convolution
                   for (int x = i-(kernal_size-1)/2 ; x < i-(kernal_size-1)/2+kernal_size ; x++)
                   {
                       for (int y = j-(kernal_size-1)/2 ; y < j-(kernal_size-1)/2+kernal_size ; y++)
                       {
                           // Get pixels
                           double B = MatImgIn.at<Vec3b>(y,x)[0], G = MatImgIn.at<Vec3b>(y,x)[1], R = MatImgIn.at<Vec3b>(y,x)[2];
                           // pixels multiply variables
                           pixelB += (B * C + C_1);
                           pixelG += (G * C + C_1);
                           pixelR += (R * C + C_1);
                           index --;
                       }
                   }
                   // Check pixel
                   pixelB = pixelCheck(pixelB);
                   pixelG = pixelCheck(pixelG);
                   pixelR = pixelCheck(pixelR);
                   // Set pixel
                   QImgOut.setPixel(i-(kernal_size+1)/2+1, j-(kernal_size+1)/2+1, qRgb(pixelR, pixelG, pixelB));
               }
           }
           // Show Image
           ui->showImgOut->setPixmap(QPixmap::fromImage(QImgOut.scaled(ui->showImgOut->width(),ui->showImgOut->height(),Qt::KeepAspectRatio)));
}
