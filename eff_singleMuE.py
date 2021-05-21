from ROOT import TChain, TH1F, Double, TFile, TH2F
import copy
import numpy as np


chain = TChain('l1UpgradeEmuTree/L1UpgradeTree', 'tree')

#for line in open('../ntuple/Run3_NuGun_MC_ntuples.list', 'r'):
for line in open('fileList.txt', 'r'):
    line = line.rstrip()

    if line.find('.root')==-1: continue

    chain.AddFile(line)

#chain.AddFile('/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/bundocka/condor/reHcalTP_PFA1p_Nu_110X_105p12_mufix_1620043913/9.root')

chain.SetBranchStatus('*', 0)
chain.SetBranchStatus('muon*', 1)
chain.SetBranchStatus('eg*', 1)


Nevt = chain.GetEntries()

print Nevt, 'events detected'

ptrange = np.arange(3, 23, 1).tolist()
etarange = np.arange(0.5, 2.6, 0.2).tolist()

#print len(ptrange), min(ptrange), max(ptrange), len(etarange), min(etarange), max(etarange)

hden = TH2F('den', 'den', len(ptrange)-1, min(ptrange), max(ptrange), len(ptrange)-1, min(ptrange), max(ptrange)) 
hnum = TH2F('num', 'num', len(ptrange)-1, min(ptrange), max(ptrange), len(ptrange)-1, min(ptrange), max(ptrange))


for evt in xrange(Nevt):
    chain.GetEntry(evt)

    if evt%1000==0: print('{0:.2f}'.format(Double(evt)/Double(Nevt)*100.), '% processed')
    
#    if evt == 100000: break
    
    muEts = [i for i in chain.muonEt]
    muEtas = [i for i in chain.muonEta]
    muIds = [i for i in chain.muonQual]

    egEts = [i for i in chain.egEt]
    egEtas = [i for i in chain.egEta]

    for ptvalm in ptrange:
        for ptvale in ptrange:
#        for etaval in etarange:


            hden.Fill(ptvalm + 0.5, ptvale + 0.5)
            flag_mu = False


            for idx, Et in enumerate(muEts):
#                if muEts[idx] >= ptval and abs(muEtas[idx]) <= etaval and muIds[idx] >= 12:
                if muEts[idx] > ptvalm and abs(muEtas[idx]) < 1.5 and muIds[idx] >= 12:
                    flag_mu = True


            flag_e = False
            for idx, Et in enumerate(egEts):
#                if muEts[idx] >= ptval and abs(muEtas[idx]) <= etaval and muIds[idx] >= 12:
                if egEts[idx] > ptvale and abs(egEtas[idx]) < 1.5:
                    flag_e = True



            if flag_mu and flag_e:
                hnum.Fill(ptvalm + 0.5, ptvale+0.5)


ratio = copy.deepcopy(hnum)
ratio.Divide(hden)
ratio.SetName('eff')
ratio.SetTitle('eff')

ratio2 = copy.deepcopy(ratio)
ratio2.Scale(2544*11200)
ratio2.SetName('rate')
ratio2.SetTitle('rate')

file = TFile('out_mue.root', 'recreate')

hden.Write()
hnum.Write()
ratio.Write()
ratio2.Write()

file.Write()
file.Close()
