import os
import matplotlib.pyplot as plt


suppress_method = ['rmall', 'mmil',"mm","1il"]
labels = ['RmAll','MM/IL','MM',"1/IL"]
#path = "/home/f4de/uni/dpp/dpp-final/"
path = "/home/chiara/Scrivania/Lezioni_ComputerScience/DP&P/dpp-final/"
dataset = path+"datasets/synthetic/ds_x100_y100_d02.csv"
dataset_name = dataset.split("/")[8].split(".")[0]

def run_script(args):
    #os.system(f"python3 /home/f4de/uni/dpp/dpp-final/anon_hkp.py {args}")
    os.system(f"python3 /home/chiara/Scrivania/Lezioni_ComputerScience/DP\&P/dpp-final/anon_hkp.py {args}")

def stat_k(k_list):
    for method in suppress_method:
        for k in k_list:
            run_script(f"-K {k} \
                         -H 0.4 \
                         -P 5 \
                         -rmt {method} \
                         --stat '{dataset_name}_k_{method}.txt' \
                         -df '{dataset}' \
                         --delta 80 \
                         -o '/dev/null'")
        graph(f"{dataset_name}_k_{method}.txt","k",k_list)
    plt.legend(labels)     
    plt.show()           

def stat_p(p_list):
    for method in suppress_method:
        for p in p_list:
            run_script(f"-K 10 \
                        -H 0.4 \
                        -P {p} \
                        -rmt {method} \
                        --stat '{dataset_name}_p_{method}.txt' \
                        -df '{dataset}' \
                        --delta 80 \
                        -o '/dev/null' ")
        graph(f"{dataset_name}_p_{method}.txt","p",p_list)
    plt.legend(labels)     
    plt.show()    

def stat_delta(delta_list):
    for method in suppress_method:
        for delta in delta_list:
            run_script(f"-K 10 \
                        -H 0.4 \
                        -P 5 \
                        -rmt {method} \
                        --stat '{dataset_name}_h_{method}.txt' \
                        -df '{dataset}' \
                        --delta {delta} \
                        -o '/dev/null' ")
        graph(f"{dataset_name}_h_{method}.txt","h",delta_list)
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

 

#stat_k([50,100,200,300,400])  # connect
#stat_k([5,10,15,20,25,30])

#stat_p([2,3,4,5,6,7])

#stat_delta([30,40,50,60,70])  # connect
stat_delta([60,70,80,90])