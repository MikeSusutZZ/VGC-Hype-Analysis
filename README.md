# VGC-Hype-Analysis
Hey everyone! I made a new meta Analysis tool to observe which pokemon are being over hyped and under explored!

This takes data from LabMaus, observes each time a pokemon hit at least 10 uses in a tournament with at least 100 players, and checks to see what percentage of them make it into the top 25% of the standings (advancement rate on LabMaus).

On average, a pokemon should have a 25% advancement rate into the top 25%. If it's more, it over performs, less means it under performed. My program gives you it's advancement rate -25, so average would be a 0, positive good, negative bad. It also says how many uses it recorded, as naturally a pokemon with more usage will end up with a more balanced number, so pokemon such as Rillaboom would be expected near 0, and a 1% deviance from that is as impactful as a 5% deviance from a rarer pokemon. (If there are stats people who know a way I can normalize for that in an effective way lmk)

I find this information valuable, as it represents the success a pokemon brings to a team regardless of how often it is brought. To say "Incineroar is the best, it was in 6/8 top 8" when 90% of the field brought it wouldn't really be fair to it's actual value. Incineroar may still in fact be the best pokemon at that event, but it's results under performed it's hype. You can think of these stats being more of a metric of how well they matched expectations.
