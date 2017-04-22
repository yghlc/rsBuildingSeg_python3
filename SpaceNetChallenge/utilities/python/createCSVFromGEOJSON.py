from spaceNetUtilities import labelTools as lT
import os
import glob
import argparse


def createCSVFromGEOJSON(rasterList,geoJsonList,outputCSVFileName):

    chipSummaryList = []

    #AOI_2_RIO_3Band_img997.tif
    #AOI_2_RIO_img635.geojson
    if len(rasterList) != len(geoJsonList):
        print 'the count the raster is not equal to geojson'
        return False

    # find RasterPrecursor
    # rasterList = glob.glob(os.path.join(rasterDirectory, '*.tif'))
    # rasterPrefix = os.path.basename(rasterList[0])
    # rasterPrefix = rasterPrefix.split("_")[0]

    # geoJsonList = glob.glob(os.path.join(geoJsonDirectory, '*.geojson'))
    for i in range(0,len(rasterList)):
        image_path = rasterList[i]
        geojson_path = geoJsonList[i]
        rasterName = os.path.basename(image_path)
        imageId = os.path.split(rasterName)[0]


        # for stripItem in stripList:
        #     rasterName = rasterName.replace(stripItem, '')


        # if args.DontstripFirstUnderScore:
        #     rasterName = rasterPrefix+"_"+rasterName.split('_',1)[1]
        # else:
        #     rasterName = rasterPrefix+"_"+rasterName
        print(imageId)
        # print(os.path.join(rasterDirectory,rasterName))
        # chipSummary = {'chipName': os.path.join(rasterDirectory, rasterName),
        #                'geoVectorName': os.path.join(geoJsonDirectory, imageId),
        #                'imageId': os.path.splitext(imageId)[0]}

        chipSummary = {'chipName': image_path,
                       'geoVectorName': geojson_path,
                       'imageId': imageId}

        chipSummaryList.append(chipSummary)

    print("starting")
    lT.createCSVSummaryFile(chipSummaryList, outputCSVFileName,
                            replaceImageID=rasterPrefix+"_",
                            createProposalsFile=createProposalFile,
                            pixPrecision=args.pixelPrecision)

    print("finished")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-imgDir", "--imgDir", type=str,
                        help="Directory of Raster Images")
    parser.add_argument("-geoDir", "--geojsonDir", type=str,
                        help="Directory of geojson files")
    parser.add_argument("-o", "--outputCSV", type=str,
                        help="Output File Name and Location for CSV")
    parser.add_argument("-pixPrecision", "--pixelPrecision", type=int,
                        help="Number of decimal places to include for pixel, uses round(xPix, pixPrecision)"
                             "Default = 2",
                        default=2)
    parser.add_argument("--CreateProposalFile", help="Create ProposalsFile",
                        action="store_true")
    parser.add_argument("-strip", "--stripOutFromGeoJson", type=str,
                        help="string delimited")
    parser.add_argument("--DontstripFirstUnderScore", action="store_false")
    args = parser.parse_args()

    rasterDirectory = args.imgDir
    geoJsonDirectory = args.geojsonDir
    outputCSVFileName = args.outputCSV
    createProposalFile = args.CreateProposalFile
    if args.stripOutFromGeoJson:
        stripList = args.stripOutFromGeoJson.split(' ')
    else:
        stripList =[]


    #band3directory = '/usr/local/share/data/AOI_1_RIO/processed2/3band'
    #band8directory = '/usr/local/share/data/AOI_1_RIO/processed2/8band'
    #geoJsonDirectory = '/usr/local/share/data/AOI_1_RIO/processed2/geojson'

    jsonList = []
    chipSummaryList = []

    #AOI_2_RIO_3Band_img997.tif
    #AOI_2_RIO_img635.geojson


    # find RasterPrecursor
    rasterList = glob.glob(os.path.join(rasterDirectory, '*.tif'))
    rasterPrefix = os.path.basename(rasterList[0])
    rasterPrefix = rasterPrefix.split("_")[0]


    geoJsonList = glob.glob(os.path.join(geoJsonDirectory, '*.geojson'))
    for imageId in geoJsonList:
        imageId = os.path.basename(imageId)
        rasterName = imageId.replace('.geojson','.tif')

        for stripItem in stripList:
            rasterName = rasterName.replace(stripItem, '')


        if args.DontstripFirstUnderScore:
            rasterName = rasterPrefix+"_"+rasterName.split('_',1)[1]
        else:
            rasterName = rasterPrefix+"_"+rasterName
        print(imageId)
        print(os.path.join(rasterDirectory,rasterName))
        chipSummary = {'chipName': os.path.join(rasterDirectory, rasterName),
                       'geoVectorName': os.path.join(geoJsonDirectory, imageId),
                       'imageId': os.path.splitext(imageId)[0]}

        chipSummaryList.append(chipSummary)

    print("starting")
    lT.createCSVSummaryFile(chipSummaryList, outputCSVFileName,
                            replaceImageID=rasterPrefix+"_",
                            createProposalsFile=createProposalFile,
                            pixPrecision=args.pixelPrecision)

    print("finished")