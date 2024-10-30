#!/bin/bash
conda activate logparser
home="$(pwd)/../logparser"

echo "=== Evaluating AEL ==="  && cd $home/AEL && python benchmark.py && \
echo "=== Evaluating Drain ===" && cd $home/Drain && python benchmark.py && \
echo "=== Evaluating IPLoM ===" && cd $home/IPLoM && python benchmark.py && \
echo "=== Evaluating LenMa ===" && cd $home/LenMa && python benchmark.py && \
echo "=== Evaluating LFA ===" && cd $home/LFA && python benchmark.py && \
echo "=== Evaluating LKE ===" && cd $home/LKE && python benchmark.py && \
echo "=== Evaluating LogCluster ===" && cd $home/LogCluster && python benchmark.py && \
echo "=== Evaluating LogMine ===" && cd $home/LogMine && python benchmark.py && \
echo "=== Evaluating LogSig ===" && cd $home/LogSig && python benchmark.py && \
echo "=== Evaluating MoLFI ===" && cd $home/MoLFI && python benchmark.py && \
echo "=== Evaluating SHISO ===" && cd $home/SHISO && python benchmark.py && \
echo "=== Evaluating SLCT ===" && cd $home/SLCT && python benchmark.py && \
echo "=== Evaluating Spell ===" && cd $home/Spell && python benchmark.py && \
# echo "=== Evaluating logmatch ===" && cd $home/logmatch && python benchmark.py &&\
# echo "=== Evaluating NuLog ===" && cd $home/NuLog && python benchmark.py &&\
echo "=== Evaluating Brain ===" && cd $home/Brain && python benchmark.py &&\
echo "=== Evaluating OSPattern ===" && cd $home/OSPattern && python benchmark.py &&\
# echo "=== Evaluating DivLog ===" && cd $home/DivLog && python benchmark.py &&\
echo "All Evaluations succeed!"