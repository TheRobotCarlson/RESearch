## Inspiration

We were inspired by recent research done by Harvard University. The researchers were able to encode a small gif in DNA, frame by frame. We thought about how we could improve this process, and make it more accessible.

## What it does

RESearch uses existing databases of genes and restriction enzymes to find the optimal way to encode arbitrary information into DNA. (Restriction enzymes are used to bread apart DNA at certain base-pair patterns.) Research essentially outputs a step by step guide for a lab scientist trying to create a specific sequence in DNA. This can be used to either store arbitrary data in DNA, or (more importantly) to easily edit existing DNA to eliminate dangerous or unwanted mutations. For example, we could edit the DNA of bacteria to eliminate their resistance to antibiotics.

## How I built it

RESearch is built mostly in python, but utilizes neo4j for the database of enzymes, and a freely available tool called Blast to easily search for patterns in genes.

## Challenges I ran into

It was very hard for us to optimize the neo4j database. There were over a million enzymes that we had to search through, so we had to modify our algorithm to allow it to run in a reasonable amount of time.

## Accomplishments that I'm proud of

- Learning new technologies, and using them to create a relatively finished project.
- Working efficiently as a team to finish the project in time.

## What I learned

We learned neo4j without any prior experience. We also learned a lot about biology and specifically bioinformatics.

## What's next for RESearch
Hopefully, we can use RESearch for some future research projects, to develop it more.

# Task list

- [x] ReBase parser (Brian)

- [x] GeneBank and ReBase local storage solutions

- [x] General binary value to DNA Encoder (David)

- [x] General DNA to binary value Decoder (David)

- [x] BLAST Subprocess caller for similarity (Christian)
  - [ ] may require clean up

- [x] XML output parser and re-entry into database (Zach)

- [ ] Search...
  - [x] substring change count
  - [ ] find initial mtch/config
  - [ ] stochastically optimize
  - [ ] more stuff

- [ ] Google slides

- [ ] Web something?

- [ ] designer pitch

- [ ] memoization + caching


# Presentation content

- Stuff to print for each step:
  - Gene used
  - Enzyme used
  - Coordinate of enzyme usage
