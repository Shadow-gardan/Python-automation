from file_organizer import organize_files
from data_processor import load_records
from report_generator import write_report


def main() -> None:
	input_directory = "data/input"
	output_directory = "data/output"

	print("Starting file organization...")
	organize_files(input_directory, output_directory)
	print("File organization completed.")

	data_file = f"{input_directory}/sales.csv"
	records = load_records(data_file)
	report_path = write_report(records, f"{output_directory}/sales_report.json")
	print(f"Processed {len(records)} data records -> {report_path}")


if __name__ == "__main__":
	main()
