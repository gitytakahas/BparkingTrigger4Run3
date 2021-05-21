from ROOT import TChain, TH1F, Double, TFile, TH2F
import copy


chain = TChain('l1UpgradeEmuTree/L1UpgradeTree', 'tree')

#for line in open('../ntuple/Run3_NuGun_MC_ntuples.list', 'r'):
for line in open('fileList.txt', 'r'):
    line = line.rstrip()

    if line.find('.root')==-1: continue

    chain.AddFile(line)

#chain.AddFile('/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/bundocka/condor/reHcalTP_PFA1p_Nu_110X_105p12_mufix_1620043913/9.root')

chain.SetBranchStatus('*', 0)
chain.SetBranchStatus('muon*', 1)


Nevt = chain.GetEntries()

print Nevt, 'events detected'

minpt = 5.
maxpt = 15.
mineta = 0.5
maxeta = 2.5

hden = TH2F('den', 'den', int(maxpt - minpt), minpt, maxpt, 10, mineta, maxeta)
hnum = TH2F('num', 'num', int(maxpt - minpt), minpt, maxpt, 10, mineta, maxeta)

for evt in xrange(Nevt):
    chain.GetEntry(evt)

    if evt%1000==0: print('{0:.2f}'.format(Double(evt)/Double(Nevt)*100.), '% processed')
    
    if evt == 100000: break
    

#    if len(chain.muonEt) == 0: continue
#    import pdb; pdb.set_trace()

    muEts = [i for i in chain.muonEt]
    muEtas = [i for i in chain.muonEta]

    for ipt in range(1, hden.GetXaxis().GetNbins()+1):
        for ieta in range(1, hden.GetYaxis().GetNbins()+1):

            ptThr = hden.GetXaxis().GetBinLowEdge(ipt)
            etaThr = hden.GetYaxis().GetBinLowEdge(ieta)
            
            # to avoid boundary bin migration
            ptval = hden.GetXaxis().GetBinLowEdge(ipt) + hden.GetXaxis().GetBinWidth(ipt)/2.
            etaval = hden.GetYaxis().GetBinLowEdge(ieta) + hden.GetYaxis().GetBinWidth(ieta)/2.

            hden.Fill(ptval, etaval)
            flag = False


            for idx, Et in enumerate(muEts):
                if muEts[idx] > ptThr and abs(muEtas[idx]) < etaThr:
                    flag = True


#            print ptThr, etaThr, flag


            if flag:
                hnum.Fill(ptval, etaval)

#    for imu in range(len(chain.muonEt)):

        ### implement here the flag for each variation 
#        if chain.muonEt[imu] > 9.:
            
#            hnum.Fill()
        
        


ratio = copy.deepcopy(hnum)
ratio.Divide(hden)
ratio.SetName('eff')
ratio.SetTitle('eff')

file = TFile('out.root', 'recreate')

hden.Write()
hnum.Write()
ratio.Write()

file.Write()
file.Close()
