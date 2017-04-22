
from osgeo import gdal, ogr
import os

def CreateGeoJSON ( fn, cluster, geom, proj ):
    """

    :param fn: IMAGE id
    :param cluster: matrix or detected result (one band)
    :param geom: the image (detected) geo information
    :param proj: the image (detected) project information
    :return:
    """
    memdrv = gdal.GetDriverByName ('MEM')
    src_ds = memdrv.Create('',cluster.shape[1],cluster.shape[0],1)
    src_ds.SetGeoTransform(geom)
    src_ds.SetProjection(proj)
    band = src_ds.GetRasterBand(1)
    band.WriteArray(cluster)
    dst_layername = "BuildingID"
    drv = ogr.GetDriverByName("geojson")

    if os.path.exists('./geojson/' + fn + dst_layername + ".geojson"):
        drv.DeleteDataSource('./geojson/' + fn + dst_layername + ".geojson")

    dst_ds = drv.CreateDataSource ( './geojson/' + fn + dst_layername + ".geojson")
    dst_layer = dst_ds.CreateLayer( dst_layername, srs=None )
    dst_layer.CreateField( ogr.FieldDefn("DN", ogr.OFTInteger) )
    gdal.Polygonize( band  , None, dst_layer, 0, ['8CONNECTED=8'], callback=None )
    return