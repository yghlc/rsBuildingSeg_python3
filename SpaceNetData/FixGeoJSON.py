from osgeo import gdal, ogr
import os

def FixGeoJSON( fn ):
    """

    :param fn: Image ID
    :return:
    """
    buf_dist = 0.0
    dst_layername = "BuildingID"
    drv = ogr.GetDriverByName("geojson")
    dst_ds = drv.Open ( './geojson.full/' + fn + dst_layername + ".geojson")
    dst_layer = dst_ds.GetLayer(0)
    if os.path.exists('./geojson.full/buffer' + fn + dst_layername + ".geojson"):
        drv.DeleteDataSource('./geojson.full/buffer' + fn + dst_layername + ".geojson")
    adst_ds = drv.CreateDataSource ( './geojson.full/buffer' + fn + dst_layername + ".geojson")
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
    return