from embedder import get_embedding
 
vec = get_embedding("Python developer with 3 years React experience")
print(f"Vector length: {len(vec)}")   # should print 1536
print(f"First 5 values: {vec[:5]}")   # should be small floats
