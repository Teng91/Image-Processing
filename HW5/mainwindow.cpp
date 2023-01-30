#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    ui->showData->setFontPointSize(12);

    // Set variable "pseudoColorTable"
    int R, G, B;
    for (int i = 0 ; i < 256 ; i++)
    {
        if (i == 0)
            R = G = B = 0;
        else
        {
            R = i;
            G = i-64;
            B = i-128;
        }
        pseudoColorTable[i][0] = int(checkPixel(R));
        pseudoColorTable[i][1] = int(checkPixel(G));
        pseudoColorTable[i][2] = int(checkPixel(B));
    }

    // Assign color bar QImages
    QImgBarGray = QImage(512, 20, QImage::Format_RGB32);
    QImgBarRGB  = QImage(512, 20, QImage::Format_RGB32);

    // Show color bars
    showColorBar();
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_actionOpen_triggered()
{
    // Open Image
    QString filePath = QFileDialog::getOpenFileName(this, tr("Open Image"), ".", tr("Images(*.bmp *.jpeg *.png *.jpg)"));
    MatImgIn = imread(filePath.toStdString());
    if (!MatImgIn.empty())
    {
        // Set up variables
        imgCols = MatImgIn.cols;
        imgRows = MatImgIn.rows;
        // Set QImgIn
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

void MainWindow::on_actionClose_triggered()
{
    QApplication::quit();
}

void MainWindow::on_RGB_clicked()
{
    // Show Img
    ui->showImgOut->setPixmap(QPixmap::fromImage(QImgIn.scaled(ui->showImgOut->width(),ui->showImgOut->height(),Qt::KeepAspectRatio)));

    // Show the transform result
    int B = MatImgIn.at<Vec3b>(0,0)[0], G = MatImgIn.at<Vec3b>(0,0)[1], R = MatImgIn.at<Vec3b>(0,0)[2];
    colorData01 = "(R, G, B) = " + QString::number(R) + ", " + QString::number(G) + ", " + QString::number(B);
    ui->showData->append(colorData01 + " ---> " + colorData01);

    // Set kmeansData for kmeans algorithm
    kmeansData = Mat(imgCols*imgRows*1, 3, CV_32F);
    label.release();
    center.release();
    for (int i = 0 ; i < imgRows ; i++)
        for (int j = 0 ; j < imgCols ; j++)
            for (int k = 0 ; k < 3 ; k++)
                kmeansData.at<float>(i + j*imgRows, k) = MatImgIn.at<Vec3b>(i,j)[k];
}

void MainWindow::on_CMY_clicked()
{
        // Set QImgOut
        QImgOut = QImage(imgCols, imgRows, QImage::Format_RGB32);
        for (int i = 0 ; i < imgCols ; i++)
        {
            for (int j = 0 ; j < imgRows ; j++)
            {
                double B = MatImgIn.at<Vec3b>(j,i)[0], G = MatImgIn.at<Vec3b>(j,i)[1], R = MatImgIn.at<Vec3b>(j,i)[2];
                // calculate C, M, Y
                double C = (255-R)/255, M = (255-G)/255, Y = (255-B)/255;
                QImgOut.setPixel(i, j, qRgb(int(C*255), int(M*255), int(Y*255)));
                // Print transform result
                if (i == 0 && j == 0)
                {
                    colorData01 = "(R, G, B) = " + QString::number(R) + ", " + QString::number(G) + ", " + QString::number(B);
                    colorData02 = "(C, M, Y) = " + QString::number(C) + ", " + QString::number(M) + ", " + QString::number(Y);
                    ui->showData->append(colorData01 + " ---> " + colorData02);
                }
            }
        }

        // Show Img and data
        ui->showImgOut->setPixmap(QPixmap::fromImage(QImgOut.scaled(ui->showImgOut->width(),ui->showImgOut->height(),Qt::KeepAspectRatio)));
}

void MainWindow::on_HSI_clicked()
{
    // Set kmean variables
        kmeansData = Mat(imgCols*imgRows*1, 3, CV_32F);
        label.release();
        center.release();
        // Set QImgOut
        QImgOut = QImage(imgCols, imgRows, QImage::Format_RGB32);
        for (int i = 0 ; i < imgRows ; i++)
        {
            for (int j = 0 ; j < imgCols ; j++)
            {
                double B = MatImgIn.at<Vec3b>(i,j)[0], G = MatImgIn.at<Vec3b>(i,j)[1], R = MatImgIn.at<Vec3b>(i,j)[2];
                // calaulate theta, H, S, I
                double theta, H, S, I;
                theta = acos((0.5*((R-G)+(R-B))) / sqrt((R-G)*(R-G) + (R-B)*(G-B)));
                if (B <= G)
                    H = theta;
                else
                    H = 360.0 - theta;
                S = 1 - 3/(R+G+B)*min(min(R,G),B);
                I = (R + G + B)/3/255;
                QImgOut.setPixel(j, i, qRgb(int(checkPixel(H)), int(checkPixel(S*255)), int(checkPixel(I*255))));
                // Set kmeansData for kmeans algorithm
                kmeansData.at<float>(i + j*imgRows, 0) = float(checkPixel(I*255));
                kmeansData.at<float>(i + j*imgRows, 1) = float(checkPixel(S*255));
                kmeansData.at<float>(i + j*imgRows, 2) = float(checkPixel(H));
                // Print transform result
                if (i == 0 && j == 0)
                {
                    colorData01 = "(R, G, B) = " + QString::number(R) + ", " + QString::number(G) + ", " + QString::number(B);
                    colorData02 = "(H, S, I) = " + QString::number(H) + ", " + QString::number(S) + ", " + QString::number(I);
                    ui->showData->append(colorData01 + " ---> " + colorData02);
                }
            }
        }
        // Show Img and data
        ui->showImgOut->setPixmap(QPixmap::fromImage(QImgOut.scaled(ui->showImgOut->width(),ui->showImgOut->height(),Qt::KeepAspectRatio)));

}

void MainWindow::on_XYZ_clicked()
{
    // Set QImgOut
        QImgOut = QImage(imgCols, imgRows, QImage::Format_RGB32);
        for (int i = 0 ; i < imgCols ; i++)
        {
            for (int j = 0 ; j < imgRows ; j++)
            {
                double B = MatImgIn.at<Vec3b>(j,i)[0], G = MatImgIn.at<Vec3b>(j,i)[1], R = MatImgIn.at<Vec3b>(j,i)[2];
                // calculate X, Y, Z
                double X, Y, Z;
                X = (0.412453*R + 0.357580*G + 0.180423*B)/255;
                Y = (0.212671*R + 0.715160*G + 0.072169*B)/255;
                Z = (0.019334*R + 0.119193*G + 0.950227*B)/255;
                QImgOut.setPixel(i, j, qRgb(int(checkPixel(X*255)), int(checkPixel(Y*255)), int(checkPixel(Z*255))));
                // Print transform result
                if (i == 0 && j == 0)
                {
                    colorData01 = "(R, G, B) = " + QString::number(R) + ", " + QString::number(G) + ", " + QString::number(B);
                    colorData02 = "(X, Y, Z) = " + QString::number(X) + ", " + QString::number(Y) + ", " + QString::number(Z);
                    ui->showData->append(colorData01 + " ---> " + colorData02);
                }
            }
        }
        // Show Img and data
        ui->showImgOut->setPixmap(QPixmap::fromImage(QImgOut.scaled(ui->showImgOut->width(),ui->showImgOut->height(),Qt::KeepAspectRatio)));

}

void MainWindow::on_LAB_clicked()
{
    // Set kmean variables
        kmeansData = Mat(imgCols*imgRows*1, 3, CV_32F);
        label.release();
        center.release();

        // Set QImgOut
        QImgOut = QImage(imgCols, imgRows, QImage::Format_RGB32);
        for (int i = 0 ; i < imgRows ; i++)
        {
            for (int j = 0 ; j < imgCols ; j++)
            {
                double B = MatImgIn.at<Vec3b>(i,j)[0], G = MatImgIn.at<Vec3b>(i,j)[1], R = MatImgIn.at<Vec3b>(i,j)[2];

                // X, Y, Z
                double X, Y, Z;
                X = (0.412453*R + 0.357580*G + 0.180423*B)/255;
                Y = (0.212671*R + 0.715160*G + 0.072169*B)/255;
                Z = (0.019334*R + 0.119193*G + 0.950227*B)/255;

                // L, A, B (D65 Light Source)
                double L, A, B_;
                L  = 116*LAB_hq_func(Y/100)-16;
                A  = 500*(LAB_hq_func(X/95.21)-LAB_hq_func(Y/100));
                B_ = 200*(LAB_hq_func(Y/100)-LAB_hq_func(Z/99.60));
                QImgOut.setPixel(j, i, qRgb(int(checkPixel(L*255)), int(checkPixel(A*255)), int(checkPixel(B_*255))));

                // Set kmeansData for kmeans algorithm
                kmeansData.at<float>(i + j*imgRows, 0) = float(checkPixel(B_*255));
                kmeansData.at<float>(i + j*imgRows, 1) = float(checkPixel(A*255));
                kmeansData.at<float>(i + j*imgRows, 2) = float(checkPixel(L*255));

                // Print transform result
                if (i == 0 && j == 0)
                {
                    colorData01 = "(R, G, B) = " + QString::number(R) + ", " + QString::number(G) + ", " + QString::number(B);
                    colorData02 = "(L, A, B) = " + QString::number(L) + ", " + QString::number(A) + ", " + QString::number(B_);
                    ui->showData->append(colorData01 + " ---> " + colorData02);
                }
            }
        }
        // Show Img and data
        ui->showImgOut->setPixmap(QPixmap::fromImage(QImgOut.scaled(ui->showImgOut->width(),ui->showImgOut->height(),Qt::KeepAspectRatio)));
}

void MainWindow::on_YUV_clicked()
{
    // Set QImgOut
        QImgOut = QImage(imgCols, imgRows, QImage::Format_RGB32);
        for (int i = 0 ; i < imgCols ; i++)
        {
            for (int j = 0 ; j < imgRows ; j++)
            {
                double B = MatImgIn.at<Vec3b>(j,i)[0], G = MatImgIn.at<Vec3b>(j,i)[1], R = MatImgIn.at<Vec3b>(j,i)[2];
                // Y, U, V
                double Y, U, V;
                Y = R * 0.299 + G * 0.587 + B * 0.114;
                U = R * -0.169 + G * -0.332 + B * 0.500 + 128.0;
                V = R * 0.500 + G * -0.419 + B * -0.0813 + 128.0;
                QImgOut.setPixel(i, j, qRgb(int(checkPixel(Y)), int(checkPixel(U)), int(checkPixel(V))));
                // Print transform result
                if (i == 0 && j == 0)
                {
                    colorData01 = "(R, G, B) = " + QString::number(R) + ", " + QString::number(G) + ", " + QString::number(B);
                    colorData02 = "(Y, U, V) = " + QString::number(Y) + ", " + QString::number(U) + ", " + QString::number(V);
                    ui->showData->append(colorData01 + " ---> " + colorData02);
                }
            }
        }
        // Show Img and data
        ui->showImgOut->setPixmap(QPixmap::fromImage(QImgOut.scaled(ui->showImgOut->width(),ui->showImgOut->height(),Qt::KeepAspectRatio)));
}

double MainWindow::checkPixel(double pixel)
{
    if (pixel > 255)
        pixel = 255;
    else if (pixel < 0)
        pixel = 0;

    return pixel;
}

double MainWindow::LAB_hq_func(double q)
{
    double output;
    if (q > 0.008856)
        output = pow(q, 1/3);
    else
        output = 7.787*q + 16/116;
    return output;
}

void MainWindow::on_pseudoColor_clicked()
{
    // Set QImgOut
    QImgOut = QImage(imgCols, imgRows, QImage::Format_RGB32);
    for (int i = 0 ; i < imgCols ; i++)
    {
        for (int j = 0 ; j < imgRows ; j++)
        {
            int GRAY = MatImgIn.at<Vec3b>(j,i)[0];
            QImgOut.setPixel(i, j, qRgb(pseudoColorTable[GRAY][0], pseudoColorTable[GRAY][1], pseudoColorTable[GRAY][2]));
        }
    }
    // Show Img and data
    ui->showImgOut->setPixmap(QPixmap::fromImage(QImgOut.scaled(ui->showImgOut->width(),ui->showImgOut->height(),Qt::KeepAspectRatio)));
}

void MainWindow::on_changeColor_clicked()
{
    // Set up variables
    int tableIndex = ui->tableIndex->text().toInt();
    int red = ui->red->text().toInt(), green = ui->green->text().toInt(), blue = ui->blue->text().toInt();

    // Set variable "pseudoColorTable"
    pseudoColorTable[tableIndex][0] = int(checkPixel(red));
    pseudoColorTable[tableIndex][1] = int(checkPixel(green));
    pseudoColorTable[tableIndex][2] = int(checkPixel(blue));

    showColorBar();
}

void MainWindow::on_kMeans_clicked()
{
    // Set up variables
    int k = ui->kMeans_k->text().toInt();
    kmeansResult = Mat(MatImgIn.size(), MatImgIn.type());

    // Kmeans Algorithm
    if (!kmeansData.empty())
    {
        kmeans(kmeansData, k, label, TermCriteria(TermCriteria::COUNT+TermCriteria::EPS, 30, 1e-6), 5, KMEANS_RANDOM_CENTERS, center);
        // Set kmeansResult
        if (!label.empty() && !center.empty())
        {
            for (int i = 0 ; i < imgRows ; i++)
            {
                for (int j = 0 ; j < imgCols ; j++)
                {
                    int index = label.at<int>(i + j*imgRows, 0);
                    for (int k = 0 ; k < 3 ; k++)
                        kmeansResult.at<Vec3b>(i, j)[k] = center.at<float>(index, k);
                }
            }
            // Show Img
            imshow("After K-means Algorithm", kmeansResult);
            waitKey();
        }
        else
            cout << "label and center are empty" << endl;
    }
    else
        cout << "kmeansData is empty" << endl;
}

void MainWindow::showColorBar()
{
    // Set QImgBarGray and QImgBarRGB pixel
    int gray = -1;
    for (int i = 0 ; i < 512 ; i ++)
    {
        if (i % 2 == 0)
            gray += 1;
        for (int j = 0 ; j < 20 ; j++)
        {
            QImgBarGray.setPixel(i, j, qRgb(gray, gray, gray));
            QImgBarRGB.setPixel(i, j, qRgb(pseudoColorTable[gray][0], pseudoColorTable[gray][1], pseudoColorTable[gray][2]));
        }
    }
    ui->barGray->setPixmap(QPixmap::fromImage(QImgBarGray.scaled(ui->showImgOut->width(),ui->showImgOut->height(),Qt::KeepAspectRatio)));
    ui->barRGB->setPixmap(QPixmap::fromImage(QImgBarRGB.scaled(ui->showImgOut->width(),ui->showImgOut->height(),Qt::KeepAspectRatio)));
}
