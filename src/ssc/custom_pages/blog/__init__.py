__all__: list[str] = []


# only import create if that's what is being imported
def __getattr__(name: str):
    if name == "create":
        from .blog import create

        globals()["create"] = create
        __all__.append("create")
        return create
    raise AttributeError(f"module {__name__} has no attribute {name}")
