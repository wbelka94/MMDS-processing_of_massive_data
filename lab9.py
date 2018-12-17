import time
import operator
import datetime

triplets_sample = []
unique_tracks = {}


class UniqueTracks:
    secId = 0
    author = 1
    trackName = 2


class Samples:
    userId = 0
    trackId = 1
    date = 2


def loadSamples():
    f = open('data/triplets_sample_20p.txt')
    i = 0
    for line in f:
        triplets_sample.append(parseRow(line))
        if i % 1000000 == 0:
            print(i)
        i += 1
    f.close()


def loadUniqueTracks():
    f = open('data/unique_tracks.txt', encoding='ISO-8859-1')
    i = 0
    for line in f:
        parsed_row = parseRow(line)
        unique_tracks[parsed_row[1]] = [parsed_row[0], parsed_row[2], parsed_row[3]]
        if i % 1000000 == 0:
            print(i)
        i += 1
    f.close()


def parseRow(row):
    row = row.replace('\n', '')
    return row.split('<SEP>')


def query1():
    result = {}
    for sample in triplets_sample:
        result[sample[Samples.trackId]] = result.get(sample[Samples.trackId], 0) + 1
    sorted_d = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
    i = 0
    for k, v in sorted_d:
        print(unique_tracks[k][UniqueTracks.trackName], " ", unique_tracks[k][UniqueTracks.author], " ", v)
        i += 1
        if i == 10:
            break


def query2():
    result = {}
    for sample in triplets_sample:
        tmp = result.get(sample[Samples.userId], {})
        tmp[sample[Samples.trackId]] = tmp.get(sample[Samples.trackId], 0) + 1
        result[sample[Samples.userId]] = tmp
    for k, v in result.items():
        result[k] = len(v)
    sorted_d = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
    i = 0
    for k, v in sorted_d:
        print(k, " ", v)
        i += 1
        if i == 10:
            break


def query3():
    result = {}
    for sample in triplets_sample:
        index = unique_tracks[sample[Samples.trackId]][UniqueTracks.author]
        result[index] = result.get(index, 0) + 1
    sorted_d = sorted(result.items(), key=operator.itemgetter(1))
    print(sorted_d[-1][0], " ", sorted_d[-1][1])


def query4():
    result = {}
    for sample in triplets_sample:
        month = datetime.datetime.fromtimestamp(int(sample[Samples.date])).month
        result[month] = result.get(month, 0) + 1
    sorted_d = sorted(result.items(), key=operator.itemgetter(0))
    for month, value in sorted_d:
        print(month, " ", value)


def query5():
    queenTracks = {}
    queenTracksPopularity = {}
    for k, track in unique_tracks.items():
        if track[UniqueTracks.author] == "Queen":
            queenTracks[k] = []
    for sample in triplets_sample:
        track = sample[Samples.trackId]
        if track in queenTracks:
            if sample[Samples.userId] not in queenTracks[track]:
                queenTracks[track].append(sample[Samples.userId])
                queenTracksPopularity[track] = queenTracksPopularity.get(track, 0) + 1
    sortedQueenTracksPopularity = sorted(queenTracksPopularity.items(), key=operator.itemgetter(1), reverse=True)
    result = {}
    trackCounter = 0
    for trackId, _ in sortedQueenTracksPopularity:
        for user in queenTracks[trackId]:
            result[user] = result.get(user, 0) + 1
        trackCounter = trackCounter + 1
        if trackCounter >= 3:
            break
    sorted_d = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
    sorted_d = sorted(sorted_d, key=operator.itemgetter(0))
    i = 0
    countOfUsers = 0
    for k, v in sorted_d:
        if v >= 3:
            if i < 10:
                print(k)
            i += 1
            countOfUsers = countOfUsers + 1
    print("Number of users: ", countOfUsers)


def main():
    globalStart = time.time()
    start = time.time()
    loadSamples()
    end = time.time()
    print("Time of loadSamples(): ", end - start)
    start = time.time()
    loadUniqueTracks()
    end = time.time()
    print("Time of loadUniqueTracks(): ", end - start)
    start = time.time()
    query1()
    end = time.time()
    print("Time of query1(): ", end - start)
    start = time.time()
    query2()
    end = time.time()
    print("Time of query2(): ", end - start)
    start = time.time()
    query3()
    end = time.time()
    print("Time of query3(): ", end - start)
    start = time.time()
    query4()
    end = time.time()
    print("Time of query4(): ", end - start)
    start = time.time()
    query5()
    end = time.time()
    print("Time of query5(): ", end - start)
    globalEnd = time.time()
    print("Total time: ", globalEnd - globalStart)


if __name__ == "__main__":
    main()