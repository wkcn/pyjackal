#coding=utf-8
from scipy.misc import imread, imsave
import matplotlib.pyplot as plt
import numpy as np

heady = 60

def read_stage(mid):
    pic = imread("Jackal-Stage%d.png" % mid)[heady:-8,:,:]
    rows, cols, tu = pic.shape

    gr = rows // 16
    gc = cols // 32
    if gr * 16 != rows or gc * 32 != cols:
        raise Exception("Error Ratio", gr * 16, rows, gc * 32, cols)

    res = set()
    arr = []
    buf = np.ones((64, 32 * 16, 4))
    tb = []
    k = 0
    need = []
    rs = [i for i in range(0, gr, 2)] + [i for i in range(1, gr, 2)]
    for r in rs:
        has_new = False
        for c in range(gc):
            pi = pic[r * 16:r * 16 + 32,c * 32:c * 32 + 32,:]

            if pi.shape[0] == 32 and pi.shape[1] == 32:
                ti = (np.ones((32,32,4)) * 255).astype(np.uint8)
                ti[:,:,:3] = pi
                '''
                bb = ti[:,:,0] * 256 * 256 + ti[:,:,1] * 256 + ti[:,:,2]
                if len(np.unique(bb)) > 4:
                    continue
                '''
                buf[16:16+32,c*32:(c+1)*32,:] = ti / 255.0
                k += 1
                sh = ti.tostring()
                if sh not in res:
                    res.add(sh)
                    has_new = True
                tb.append(ti)
        '''
        plt.title("%d" % r)
        plt.imshow(buf)
        plt.show()
        '''
        if has_new:
            arr.extend(tb)
        else:
            print ("Ignore: %d" % r)
        tb = []
    print (len(arr), k)
    cc = 16
    rr = (len(arr) + 15) // 16
    out = np.zeros((rr * 32, cc * 32, 4)).astype(np.double)
    r = 0
    c = 0
    print (rr, cc, rr * cc, len(arr))

    four = []
    for ti in arr:
        bb = ti[:,:,0] * 256 * 256 + ti[:,:,1] * 256 + ti[:,:,2]
        if len(np.unique(bb)) <= 4:
            four.append(ti)

    for ti in arr:
        bb = ti[:,:,0] * 256 * 256 + ti[:,:,1] * 256 + ti[:,:,2]
        if len(np.unique(bb)) > 4:
            # remove background color
            b1 = (ti[:,:,0] == 255) & (ti[:,:,1] == 162) & (ti[:,:,2] == 0)
            b2 = (ti[:,:,0] == 198) & (ti[:,:,1] == 113) & (ti[:,:,2] == 0)
            b = (b1 | b2)
            ti[b, :] = 0.0
            '''
            bestne = -np.inf
            best = None
            beb = None
            for mp in four:
                eb = (ti == mp).all(2)
                ne = np.sum(eb)
                if ne > bestne:
                    bestne = ne
                    best = mp
                    beb = eb
            #ti[beb, :] = 0
            '''
            #plt.subplot(121)
            #plt.imshow(ti)
            #plt.subplot(122)
            #plt.imshow(best)
            #plt.show()


    for im in arr:
        out[r * 32:(r + 1) * 32, c * 32:(c + 1) * 32, :] = im / 255.0
        c += 1
        if c == 16:
            c = 0
            r += 1
    imsave("stagef%d_map.png" % (mid), out)
    print ("ok")

read_stage(1)
