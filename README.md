# OPRF-PSI Python Example

Private set intersection (PSI) using oblivious pseudorandom functions is a technique for two parties
to share knowledge of overlapping audiences without revealing to the other their full audience. This 
is an example implementation in python.

- [Private set intersection](https://en.wikipedia.org/wiki/Private_set_intersection)
- [Oblivious pseudorandom function (OPRF)](https://en.wikipedia.org/wiki/Oblivious_pseudorandom_function) 

## Overview

![Sequence diagram](./docs/alicebob.drawio.png)

An Agent can perform both `Server` and `Client` behavior. In this example Alice is acting as 
`Server` and Bob is acting as `Client`.

(**Note**: in this sequence I refer to OPRF as "hashing" because it's shorter)

**Sequence:**
1. The `Server` uses EC to hash raw values into a hashed set, which is shared with the `Client`
   without revealing the raw data.
2. The `Client` uses EC to blind its own values before sending to the `Server` to be hashed
3. The `Server` hashes the blinded values using the same method used in step 1.
4. The `Client` unblinds the blinded+hashed values revealing the hashed value. This is used to check
   if their own values are present in the shared set.

## Usage

```
./Scripts/activate
pip install -r requirements.txt
python main.py
```

![Example terminal output](./docs/psi-example.png)