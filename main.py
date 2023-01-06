import pandas as pd
import anon_hkp as hkp
import logging, sys  # print debug and info
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="print debug info", action='store_true')
    parser.add_argument("--h", type=float, default=0.3)
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--p", type=int, default=3)
    parser.add_argument("--l", type=int, default=3)
    parser.add_argument('-s', '--sensitive', nargs='+', help='List of sensitive items', default=[0, 5, 9, 15, 17, 18, 19])
    parser.add_argument("--df", help="Dataset to anonymize", default="datasets/dataBMS1_transaction.csv")
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(format='%(asctime)s %(message)s', stream=sys.stderr, level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(asctime)s %(message)s', stream=sys.stderr, level=logging.INFO)

    # import dataset
    #filename = "datasets/dataBMS1_transaction.csv"
    #filename = "datasets/test.csv"
    filename = args.df
    h = args.h
    k = args.k
    p = args.p
    l = args.l

    df = pd.read_csv(filename)
    val1 = [i for i in range(20,df.shape[1])]
    df.drop(df.columns[val1],inplace=True,axis=1)
    # add indexes
    df.columns = [ i for i in range(len(df.columns)) ]

    sensitive = args.sensitive
    anon = hkp.anon_hkp(df,sensitive,h,k,p,l)

    # preprocessing
    logging.info("start preprocessing")
    anon.suppress_size1_mole()
    logging.info("end preprocessing")
    # find minimal moles
    logging.info("start finding minimal moles")
    Ms = anon.find_minimal_moles()
    logging.info("end finding minimal moles")
    #print("Minimal moles to suppress: ",Ms)
    logging.info("start suppressing mole")
    supp_item = anon.suppress_minimal_moles(Ms)
    logging.info("end suppressing mole")
    #print(anon.MM)


