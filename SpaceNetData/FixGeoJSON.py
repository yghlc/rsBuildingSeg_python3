from osgeo import gdal, ogr
import os

def FixGeoJSON(file_path,save_folder):
    """

    :param file_path: geojson file path, like './geojson.full/' + fn + dst_layername + ".geojson"
    :return:
    """
    if os.path.isfile(file_path) is False:
        print 'error, file %s not exist'%file_path
        return False

    save_path = os.path.join(save_folder,os.path.basename(file_path))

    buf_dist = 0.0
    dst_layername = "BuildingID"
    drv = ogr.GetDriverByName("geojson")
    dst_ds = drv.Open (file_path)
    dst_layer = dst_ds.GetLayer(0)
    if os.path.exists(save_path):
        drv.DeleteDataSource(save_path)
    adst_ds = drv.CreateDataSource (save_path)
    adst_layer = adst_ds.CreateLayer( dst_layername, srs=None )
    adst_layer.CreateField( ogr.FieldDefn("DN", ogr.OFTInteger) )

    for i in range(dst_layer.GetFeatureCount()):
        f = dst_layer.GetFeature(i)
        clusternumber = f.GetField("DN")
        f.SetGeometry(f.GetGeometryRef().Buffer(buf_dist))
        if 0 == f.GetField("DN"):
            dst_layer.DeleteFeature(i) #not supported by geoJSON driver now
        else:
            adst_layer.CreateFeature(f)
    return save_path