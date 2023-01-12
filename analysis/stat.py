import os
import matplotlib.pyplot as plt


suppress_method = ['rmall', 'mmil',"mm","1il"]
labels = ['RmAll','MM/IL','MM',"1/IL"]
path = "/home/f4de/uni/dpp/dpp-final/"
dataset = path+"datasets/preproc_dataBMS1_transaction.csv"
dataset_name = dataset.split("/")[7].split(".")[0]

def run_script(args):
    os.system(f"python3 /home/f4de/uni/dpp/dpp-final/anon_hkp.py {args}")

def stat_k(k_list):
    for method in suppress_method:
        for k in k_list:
            run_script(f"-K {k} \
                        -rmt {method} \
                        --stat '{dataset_name}_k_{method}.txt' \
                        -df '{dataset}' \
                        -o '/dev/null' ")
        graph(f"{dataset_name}_k_{method}.txt","k",k_list)
    plt.legend(labels)     
    plt.show()           

def stat_p(p_list):
    for method in suppress_method:
        for p in p_list:
            run_script(f"-P {p} \
                        -rmt {method} \
                        --stat '{dataset_name}_p_{method}.txt' \
                        -df '{dataset}' \
                        -o '/dev/null' ")
        graph(f"{dataset_name}_p_{method}.txt","p",p_list)
    plt.legend(labels)     
    plt.show()    

def stat_h(h_list):
    for method in suppress_method:
        for h in h_list:
            run_script(f"-H {h} \
                        -rmt {method} \
                        --stat '{dataset_name}_h_{method}.txt' \
                        -df '{dataset}' \
                        -o '/dev/null' ")
        graph(f"{dataset_name}_h_{method}.txt","h",h_list)
    plt.legend(labels)         
    plt.show()    

def graph(filename,param,param_list):

    x = []
    y = []
    i = 0
    for line in open(filename, 'r'):
        x.append(param_list[i])
        y.append(float(line))
        i += 1
    plt.title(f"Distorsion vs {param}")
    plt.xlabel(f"{param}")
    plt.ylabel('distorsion N/S')
    plt.yticks(y)
    plt.plot(x, y, marker = 'x')

 

stat_k([1,2,3,4])

#stat_p([1,2,3,4])
#
#stat_h([0.1,0.2,0.3,0.4])