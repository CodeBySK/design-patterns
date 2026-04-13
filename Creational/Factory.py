# =============================================================================
# FACTORY METHOD PATTERN
# Defines an interface for creating an object, but lets subclasses decide
# which class to instantiate. Decouples object creation from usage.
# =============================================================================


# =============================================================================
# WITHOUT Factory Method — Problem
# The client contains a growing if/elif block to decide which object to build.
# Adding a new type forces you to modify client code everywhere it appears.
# =============================================================================

class PDFReport_NoPattern:
    def generate(self, data):
        return f"[PDF Report] {data}"

class CSVReport_NoPattern:
    def generate(self, data):
        return f"[CSV Report] {data}"

class ExcelReport_NoPattern:
    def generate(self, data):
        return f"[Excel Report] {data}"


def create_report_no_pattern(report_type: str, data: str):
    # Every new format forces a change here AND in every other place
    # this logic is duplicated across the codebase.
    if report_type == "pdf":
        report = PDFReport_NoPattern()
    elif report_type == "csv":
        report = CSVReport_NoPattern()
    elif report_type == "excel":
        report = ExcelReport_NoPattern()
    else:
        raise ValueError(f"Unknown report type: {report_type}")
    return report.generate(data)


def without_factory():
    print("--- WITHOUT Factory Method ---")
    print(create_report_no_pattern("pdf",   "Q1 Sales"))
    print(create_report_no_pattern("csv",   "Q1 Sales"))
    print(create_report_no_pattern("excel", "Q1 Sales"))


# =============================================================================
# WITH Factory Method — Solution
# Each concrete creator encapsulates its own instantiation logic.
# Adding a new format only requires a new subclass — zero changes elsewhere.
# =============================================================================

from abc import ABC, abstractmethod


class Report(ABC):
    @abstractmethod
    def generate(self, data: str) -> str:
        pass


class PDFReport(Report):
    def generate(self, data: str) -> str:
        return f"[PDF Report] {data}"

class CSVReport(Report):
    def generate(self, data: str) -> str:
        return f"[CSV Report] {data}"

class ExcelReport(Report):
    def generate(self, data: str) -> str:
        return f"[Excel Report] {data}"


class ReportCreator(ABC):
    # Factory Method — subclasses override this to return the right product.
    @abstractmethod
    def create_report(self) -> Report:
        pass

    def deliver(self, data: str) -> str:
        report = self.create_report()   # delegate creation to the subclass
        return report.generate(data)


class PDFReportCreator(ReportCreator):
    def create_report(self) -> Report:
        return PDFReport()

class CSVReportCreator(ReportCreator):
    def create_report(self) -> Report:
        return CSVReport()

class ExcelReportCreator(ReportCreator):
    def create_report(self) -> Report:
        return ExcelReport()


def with_factory():
    print("\n--- WITH Factory Method ---")
    creators = [PDFReportCreator(), CSVReportCreator(), ExcelReportCreator()]
    for creator in creators:
        print(creator.deliver("Q1 Sales"))


if __name__ == "__main__":
    without_factory()
    with_factory()
