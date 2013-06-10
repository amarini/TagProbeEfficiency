import FWCore.ParameterSet.Config as cms

##                      _              _       
##   ___ ___  _ __  ___| |_ __ _ _ __ | |_ ___ 
##  / __/ _ \| '_ \/ __| __/ _` | '_ \| __/ __|
## | (_| (_) | | | \__ \ || (_| | | | | |_\__ \
##  \___\___/|_| |_|___/\__\__,_|_| |_|\__|___/
##                                              
########################
MC_flag = True
#GLOBAL_TAG = "FT42_V24_AN1::All"
#GLOBAL_TAG = "START53_V7D::All"
GLOBAL_TAG = 'START42_V14B::All'
OUTPUT_FILE_NAME = "Photon_tagProbeTree.root"
RECOProcess = "RECO"

##    ___            _           _      
##   |_ _|_ __   ___| |_   _  __| | ___ 
##    | || '_ \ / __| | | | |/ _` |/ _ \
##    | || | | | (__| | |_| | (_| |  __/
##   |___|_| |_|\___|_|\__,_|\__,_|\___|

process = cms.Process("TagProbe")
#stuff needed for prescales
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = GLOBAL_TAG
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
##process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True),
##                                     SkipEvent = cms.untracked.vstring('ProductNotFound')
##                                     )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

##   ____             _ ____                           
##  |  _ \ ___   ___ | / ___|  ___  _   _ _ __ ___ ___ 
##  | |_) / _ \ / _ \| \___ \ / _ \| | | | '__/ __/ _ \
##  |  __/ (_) | (_) | |___) | (_) | |_| | | | (_|  __/
##  |_|   \___/ \___/|_|____/ \___/ \__,_|_|  \___\___|
##  

readFiles = cms.untracked.vstring()

process.source = cms.Source("PoolSource", 
                            fileNames = readFiles
                            )
readFiles.extend([
'file:/afs/cern.ch/user/p/peruzzi/work/SkimZuugEventFile_9_2_8X8.root'
    ])

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )    
process.source.inputCommands = cms.untracked.vstring("keep *","drop *_MEtoEDMConverter_*_*")


process.ZuugSelection = cms.EDFilter("ZuugSelFilter",
                                       src_muons = cms.untracked.InputTag("muons"),
                                       src_photons = cms.untracked.InputTag("photons")
                                       )

process.dump=cms.EDAnalyzer('EventContentAnalyzer')




##     ___           _       _   _             
##    |_ _|___  ___ | | __ _| |_(_) ___  _ __  
##     | |/ __|/ _ \| |/ _` | __| |/ _ \| '_ \ 
##     | |\__ \ (_) | | (_| | |_| | (_) | | | |
##    |___|___/\___/|_|\__,_|\__|_|\___/|_| |_|

                                         
#  Isolation ################
#ECAL and HCAL only
if MC_flag==True:
    process.photonID = cms.EDFilter("PhotonRefSelector",
                                    src = cms.InputTag("ZuugSelection:ZuugSelPhotons"),
                                    cut = cms.string(
        "(ecalRecHitSumEtConeDR03 < (0.012*pt + 4))"
        " && (hcalTowerSumEtConeDR03 < (0.005*pt + 4 ))"
        " && (trkSumPtHollowConeDR03 < (0.002*pt + 4))"
        " && (hadronicOverEm<0.05)"
        " && (abs(superCluster.eta)>1.4442 || 0.87*sigmaIetaIeta+0.0011<0.011) && (abs(superCluster.eta)<1.566 || 0.99*sigmaIetaIeta<0.030)"
        )
                                    )
else:
    process.photonID = cms.EDFilter("PhotonRefSelector",
                                    src = cms.InputTag("ZuugSelection:ZuugSelPhotons"),
                                    cut = cms.string(
        "(ecalRecHitSumEtConeDR03 < (0.012*pt + 4))"
        " && (hcalTowerSumEtConeDR03 < (0.005*pt + 4 ))"
        " && (trkSumPtHollowConeDR03 < (0.002*pt + 4))"
        " && (hadronicOverEm<0.05)"
        " && (abs(superCluster.eta)>1.4442 || sigmaIetaIeta<0.011) && (abs(superCluster.eta)<1.566 || sigmaIetaIeta<0.030)"
        )
                                    )

process.photonPixelVeto = cms.EDFilter("PhotonRefSelector",
                                       src = cms.InputTag("ZuugSelection:ZuugSelPhotons"),
                                       cut = cms.string(str(process.photonID.cut.value())+' && (hasPixelSeed==0)')
                                       )

##    _____      _                        _  __     __             
##   | ____|_  _| |_ ___ _ __ _ __   __ _| | \ \   / /_ _ _ __ ___ 
##   |  _| \ \/ / __/ _ \ '__| '_ \ / _` | |  \ \ / / _` | '__/ __|
##   | |___ >  <| ||  __/ |  | | | | (_| | |   \ V / (_| | |  \__ \
##   |_____/_/\_\\__\___|_|  |_| |_|\__,_|_|    \_/ \__,_|_|  |___/
##   



##    _____             ____        __ _       _ _   _             
##   |_   _|_ _  __ _  |  _ \  ___ / _(_)_ __ (_) |_(_) ___  _ __  
##     | |/ _` |/ _` | | | | |/ _ \ |_| | '_ \| | __| |/ _ \| '_ \ 
##     | | (_| | (_| | | |_| |  __/  _| | | | | | |_| | (_) | | | |
##     |_|\__,_|\__, | |____/ \___|_| |_|_| |_|_|\__|_|\___/|_| |_|
##              |___/                                              

process.load("RecoLocalCalo.EcalRecAlgos.EcalSeverityLevelESProducer_cfi")

process.dimuons = cms.EDProducer("CandViewShallowCloneCombiner",
                               checkCharge = cms.bool(True),
                               cut = cms.string('mass > 0'),
                               decay = cms.string('ZuugSelection:ZuugSelMuons@+ ZuugSelection:ZuugSelMuons@-')
                               )


process.photon_sequence = cms.Sequence(
    process.ZuugSelection +
    process.photonID +
    process.photonPixelVeto +
    process.dimuons
    )


##    _____ ___   ____    ____       _          
##   |_   _( _ ) |  _ \  |  _ \ __ _(_)_ __ ___ 
##     | | / _ \/\ |_) | | |_) / _` | | '__/ __|
##     | || (_>  <  __/  |  __/ (_| | | |  \__ \
##     |_| \___/\/_|     |_|   \__,_|_|_|  |___/
##                                              
##   
#  Tag & probe selection ######
process.tagPhoton = cms.EDProducer("CandViewShallowCloneCombiner",
                                   decay = cms.string("dimuons photonID"),
                                   checkCharge = cms.bool(False),
                                   cut = cms.string("pt > 0")
                                   )
process.tagphotonPixelVeto = process.tagPhoton.clone()
process.tagphotonPixelVeto.decay = cms.string("dimuons photonPixelVeto")

process.allTagsAndProbes = cms.Sequence(
    process.tagPhoton +
    process.tagphotonPixelVeto
)


##    __  __  ____   __  __       _       _               
##   |  \/  |/ ___| |  \/  | __ _| |_ ___| |__   ___  ___ 
##   | |\/| | |     | |\/| |/ _` | __/ __| '_ \ / _ \/ __|
##   | |  | | |___  | |  | | (_| | || (__| | | |  __/\__ \
##   |_|  |_|\____| |_|  |_|\__,_|\__\___|_| |_|\___||___/
##                                                        

process.McMatchMuon = cms.EDProducer("MCTruthDeltaRMatcherNew",
    matchPDGId = cms.vint32(13),
    src = cms.InputTag("ZuugSelection:ZuugSelMuons"),
    distMin = cms.double(0.3),
    matched = cms.InputTag("genParticles"),
    checkCharge = cms.bool(False)
)
process.McMatchPhoton = process.McMatchMuon.clone()
process.McMatchPhoton.matchPDGId = cms.vint32(22)
process.McMatchPhoton.src = cms.InputTag("photonID")
process.McMatchPixelVeto = process.McMatchMuon.clone()
process.McMatchPixelVeto.matchPDGId = cms.vint32(22)
process.McMatchPixelVeto.src = cms.InputTag("photonPixelVeto")

process.zToMuMuMCMatch = cms.EDProducer( "MCTruthCompositeMatcherNew",
                                         src = cms.InputTag("dimuons"),
                                         matchMaps =  cms.VInputTag(cms.InputTag("McMatchMuon")),
                                         matchPDGId = cms.vint32()
                                         )


process.mc_sequence = cms.Sequence(
   process.McMatchMuon +
   process.McMatchPhoton +
   process.McMatchPixelVeto +
   process.dimuons +
   process.zToMuMuMCMatch 
)

############################################################################
##    _____           _       _ ____            _            _   _  ____  ##
##   |_   _|_ _  __ _( )_ __ ( )  _ \ _ __ ___ | |__   ___  | \ | |/ ___| ##
##     | |/ _` |/ _` |/| '_ \|/| |_) | '__/ _ \| '_ \ / _ \ |  \| | |  _  ##
##     | | (_| | (_| | | | | | |  __/| | | (_) | |_) |  __/ | |\  | |_| | ##
##     |_|\__,_|\__, | |_| |_| |_|   |_|  \___/|_.__/ \___| |_| \_|\____| ##
##              |___/                                                     ##
##                                                                        ##
############################################################################
##    ____                      _     _           
##   |  _ \ ___ _   _ ___  __ _| |__ | | ___  ___ 
##   | |_) / _ \ | | / __|/ _` | '_ \| |/ _ \/ __|
##   |  _ <  __/ |_| \__ \ (_| | |_) | |  __/\__ \
##   |_| \_\___|\__,_|___/\__,_|_.__/|_|\___||___/


## I define some common variables for re-use later.
## This will save us repeating the same code for each efficiency category

ZVariablesToStore = cms.PSet(
    eta = cms.string("eta"),
    pt  = cms.string("pt"),
    phi  = cms.string("phi"),
#    et  = cms.string("et"),
#    e  = cms.string("energy"),
#    p  = cms.string("p"),
#    px  = cms.string("px"),
#    py  = cms.string("py"),
#    pz  = cms.string("pz"),
#    theta  = cms.string("theta"),    
#    vx     = cms.string("vx"),
#    vy     = cms.string("vy"),
#    vz     = cms.string("vz"),
#    rapidity  = cms.string("rapidity"),
    mass  = cms.string("mass"),
#    mt  = cms.string("mt"),    
)   


DiMuonVariablesToStore = cms.PSet(
    eta = cms.string("eta"),
    pt  = cms.string("pt"),
    phi  = cms.string("phi"),
    mass  = cms.string("mass"),
#    px  = cms.string("px"),
#    py  = cms.string("py"),
#    pz  = cms.string("pz"),
#    ## super cluster quantities
#    sc_energy = cms.string("superCluster.energy"),
#    sc_et     = cms.string("superCluster.energy*sin(superCluster.position.theta)"),    
#    sc_eta    = cms.string("superCluster.eta"),
#    sc_phi    = cms.string("superCluster.phi"),
)


ProbePhotonVariablesToStore = cms.PSet(
        probe_eta = cms.string("eta"),
        probe_phi  = cms.string("phi"),
        probe_pt  = cms.string("pt"),
#        probe_px  = cms.string("px"),
#        probe_py  = cms.string("py"),
#        probe_pz  = cms.string("pz"),
        ## isolation 
        probe_trkSumPtHollowConeDR03 = cms.string("trkSumPtHollowConeDR03"),
        probe_ecalRecHitSumEtConeDR03  = cms.string("ecalRecHitSumEtConeDR03"),
        probe_hcalTowerSumEtConeDR03  = cms.string("hcalTowerSumEtConeDR03"),
#        probe_trkSumPtHollowConeDR04 = cms.string("trkSumPtHollowConeDR04"),
#        probe_ecalRecHitSumEtConeDR04  = cms.string("ecalRecHitSumEtConeDR04"),
#        probe_hcalTowerSumEtConeDR04  = cms.string("hcalTowerSumEtConeDR04"),
        ## booleans
#        probe_isPhoton  = cms.string("isPhoton"),     
        ## Hcal energy over Ecal Energy
        probe_hadronicOverEm = cms.string("hadronicOverEm"),
        ## Cluster shape information
        probe_sigmaIetaIeta_NOTSCALED = cms.string("sigmaIetaIeta"),
        ## Pixel seed
        probe_hasPixelSeed = cms.string("hasPixelSeed"),
        probe_sc_energy = cms.string("superCluster.energy"),
        probe_sc_et     = cms.string("superCluster.energy*sin(superCluster.position.theta)"),    
        probe_sc_eta    = cms.string("superCluster.eta"),
        probe_sc_phi    = cms.string("superCluster.phi")
)


CommonStuffForPhotonProbe = cms.PSet(
   variables = cms.PSet(ProbePhotonVariablesToStore),
   ignoreExceptions =  cms.bool (False),
   #fillTagTree      =  cms.bool (True),
   addRunLumiInfo   =  cms.bool (True),
   addEventVariablesInfo   =  cms.bool (True),
   pairVariables =  cms.PSet(ZVariablesToStore),
   pairFlags     =  cms.PSet(
#          mass60to120 = cms.string("60 < mass < 120")
    ),
    tagVariables   =  cms.PSet(DiMuonVariablesToStore),
    tagFlags     =  cms.PSet(
#          flag = cms.string("pt>0")
    ),    
)



if MC_flag:
    mcTruthCommonStuff = cms.PSet(
        isMC = cms.bool(MC_flag),
        tagMatches = cms.InputTag("zToMuMuMCMatch"),
        motherPdgId = cms.vint32(),
        makeMCUnbiasTree = cms.bool(MC_flag),
        checkMotherInUnbiasEff = cms.bool(MC_flag),
        mcVariables = cms.PSet(
        probe_eta = cms.string("eta"),
        probe_pt  = cms.string("pt"),
        probe_phi  = cms.string("phi"),
#        probe_mass  = cms.string("mass"),
#        probe_et  = cms.string("et"),
#        probe_e  = cms.string("energy"),
#        probe_p  = cms.string("p"),
#        probe_px  = cms.string("px"),
#        probe_py  = cms.string("py"),
#        probe_pz  = cms.string("pz"),
#        probe_theta  = cms.string("theta"),    
#        probe_vx     = cms.string("vx"),
#        probe_vy     = cms.string("vy"),
#        probe_vz     = cms.string("vz"),   
#        probe_charge = cms.string("charge"),
#        probe_rapidity  = cms.string("rapidity"),    
#        probe_mass  = cms.string("mass"),
#        probe_mt  = cms.string("mt")
        ),
        mcFlags     =  cms.PSet(
#        probe_flag = cms.string("pt>0")
        ),      
        )
else:
    mcTruthCommonStuff = cms.PSet(
        isMC = cms.bool(False)
        )


##    ___                 ___    _ 
##  |_ _|___  ___       |_ _|__| |
##   | |/ __|/ _ \       | |/ _` |
##   | |\__ \ (_) |  _   | | (_| |
##   |___|___/\___/  ( ) |___\__,_|
##                   |/            
##  Photon --> isolation, id  etc.

process.PhotonToIsoId = cms.EDAnalyzer("TagProbeFitTreeProducer",
    ## pick the defaults
    mcTruthCommonStuff,
    CommonStuffForPhotonProbe,
    # choice of tag and probe pairs, and arbitration                 
    tagProbePairs = cms.InputTag("tagPhoton"),
    arbitration   = cms.string("None"),                      
    flags = cms.PSet(
        probe_passingPixelVeto = cms.InputTag("photonPixelVeto")
    ),
    probeMatches  = cms.InputTag("McMatchPhoton"),
    allProbes     = cms.InputTag("photonID")
)


process.tree_sequence = cms.Sequence(
    process.PhotonToIsoId
    )    

##    ____       _   _     
##   |  _ \ __ _| |_| |__  
##   | |_) / _` | __| '_ \ 
##   |  __/ (_| | |_| | | |
##   |_|   \__,_|\__|_| |_|
##


if MC_flag:
    process.tagAndProbe = cms.Path(
        process.photon_sequence +
        process.allTagsAndProbes +
        process.mc_sequence + 
        process.tree_sequence
        )
else:
    process.tagAndProbe = cms.Path(
        process.photon_sequence +
        process.allTagsAndProbes +
        process.tree_sequence
        )

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string(OUTPUT_FILE_NAME)
                                   )
