import os

TRUE_VALUES = [True, "True", "true", "1", 1]
SUPPRESS_WARNINGS = os.getenv("SUPPRESS_WARNINGS", False) in TRUE_VALUES
