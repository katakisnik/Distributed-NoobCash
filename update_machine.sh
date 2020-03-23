#!/usr/bin/env bash
rsync -ra --delete ../Distributed-NoobCash/ user@192.168.1.1:Distributed-NoobCash/
rsync -ra --delete ../Distributed-NoobCash/* user@192.168.1.2:Distributed-NoobCash/
rsync -ra --delete ../Distributed-NoobCash/* user@192.168.1.3:Distributed-NoobCash/
rsync -ra --delete ../Distributed-NoobCash/* user@192.168.1.4:Distributed-NoobCash/
