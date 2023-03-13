from tiny3d.utils.registry import ModuleFactory
from tiny3d.utils.config import parse_config
from tiny3d.core import Database
from tiny3d.utils.logger import get_logger

def main():
    args, pipeline = parse_config()
    logger = get_logger()
    print(args)
    if args.list_modules:
        print("Current system contains the modules below:")
        for k, v in ModuleFactory.registry.items():
            print('\t', k)
    if args.doc is not None:
        print(ModuleFactory.registry[args.doc].__doc__)
    if pipeline is not None:
        database = Database()
        for module_config in pipeline:
            module = ModuleFactory.create_module(name=module_config['type'], database=database, **module_config['config'])
            logger.info(f"Module {module_config['name']} with type {module_config['type']} created, start execution...")
            module.execute()
            logger.info(f"Module {module_config['name']} with type {module_config['type']} execution finished.")

if __name__ == '__main__':
    main()
