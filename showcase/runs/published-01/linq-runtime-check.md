# LINQ Reporting runtime check

Showcase: `showcase/runs/published-01/showcase.md` · rules: `examples/error-correction.md` (J1, J9) · jar: `aspose-words-26.10-jdk17.jar` · Java: `openjdk version "17.0.21" 2026-10-20`

Compilation does not check LINQ Reporting templates; `ReportingEngine` parses them at run time. Each case below builds the template the answer describes, runs the answer's Java code (or, for a template given only in prose, a `JsonDataSource` with matching data) and checks the generated document: no tags left and the expected values present. Without a license, Aspose.Words adds evaluation notices to the output; they are ignored. Generated with `python showcase/scripts/check_linq_runtime.py`.

| Case | Result | Notes |
| --- | --- | --- |
| linq-reporting-01 | passed | output contains the expected values |
| linq-reporting-02 | passed | output contains the expected values |
| linq-reporting-03 | passed | output contains the expected values |
| linq-reporting-04 | passed | output contains the expected values |
| linq-reporting-05 | passed | output contains the expected values |
| linq-reporting-06 | passed | output contains the expected values |
| linq-reporting-07 | passed | output contains the expected values |
| linq-reporting-08 | not applicable | comparison only; no template or code to run |
| rule-J1-right | passed | output contains the expected values |
| rule-J9-wrong | passed | fails at run time as the rule says: Exception in thread "main" java.lang.IllegalArgumentException: A data source object must be of a visible type or implement 'interface java.lang.Iterable'. |
| rule-J9-right | passed | output contains the expected values |

## linq-reporting-01: What is the LINQ Reporting Engine in Aspose.Words?

Template:

```text
<<if [Customer.IsActive]>>
  Hello, <<[Customer.Name]>>
<<else>>
  Customer account is inactive
<</if>>

<<foreach [in Orders]>>
  <<[Name]>> — <<[Price]>>
<</foreach>>
```

Run: `ReportingEngine.buildReport` with a `JsonDataSource` (no name):

```json
{
  "Customer": {
    "IsActive": true,
    "Name": "Ann"
  },
  "Orders": [
    {
      "Name": "Pen",
      "Price": 5
    },
    {
      "Name": "Book",
      "Price": 12
    }
  ]
}
```

Text of `report.docx` (evaluation notices removed):

```text
  Hello, Ann
  Pen — 5
  Book — 12
```

Result: **passed**: output contains the expected values

## linq-reporting-02: How to generate reports using the LINQ Reporting Engine in Java?

Run: `java GenerateReport `

Text of `report.docx` (evaluation notices removed):

```text
Hello Avery!
```

Result: **passed**: output contains the expected values

## linq-reporting-03: How to create a Word document from a LINQ Reporting template and data source using Aspose.Words ReportingEngine in Java?

Template:

```text
<<[sender.getName()]>> says: “<<[sender.getMessage()]>>”
```

Run: `java BuildReportFromTemplate `

Text of `report.docx` (evaluation notices removed):

```text
Aspose says: “Hello World”
```

Result: **passed**: output contains the expected values

## linq-reporting-04: How to populate a LINQ Reporting template with data using Aspose.Words ReportingEngine.buildReport in Java?

Template:

```text
Hello, <<[sender.getName()]>>!
```

Run: `java BuildReportFromTemplate `

Text of `report.docx` (evaluation notices removed):

```text
Hello, Avery!
```

Result: **passed**: output contains the expected values

## linq-reporting-05: How to use LINQ expressions in a Word document template?

Template:

```text
Orders over 100:
<<foreach [o in data.getOrders().where(x => x.getTotal() > 100)]>>
<<[o.getName()]>> — <<[o.getTotal()]>>
<</foreach>>
```

Run: `java CreateReport `

Text of `report.docx` (evaluation notices removed):

```text
Orders over 100:
Notebook — 150
```

Result: **passed**: output contains the expected values

## linq-reporting-06: How to use loops and conditions in LINQ Reporting Engine templates?

Template:

```text
<<foreach [order in orders]>>
Order: <<[order.Id]>>

<<if [order.Total > 100]>>
Eligible for a discount.
<<else>>
Standard pricing.
<</if>>

Items:
<<foreach [item in order.Items]>>
- <<[item.Name]>>
<</foreach>>
<</foreach>>
```

Run: `ReportingEngine.buildReport` with a `JsonDataSource` ("orders"):

```json
[
  {
    "Id": 1,
    "Total": 150,
    "Items": [
      {
        "Name": "Laptop"
      }
    ]
  },
  {
    "Id": 2,
    "Total": 40,
    "Items": [
      {
        "Name": "Mouse"
      },
      {
        "Name": "Cable"
      }
    ]
  }
]
```

Text of `report.docx` (evaluation notices removed):

```text
Order: 1
Eligible for a discount.
Items:
- Laptop
Order: 2
Standard pricing.
Items:
- Mouse
- Cable
```

Result: **passed**: output contains the expected values

## linq-reporting-07: How to generate reports from JSON or XML data in Java?

Template:

```text
<<[Name]>>
```

Data `data.json`: `{"Name": "Aspose JSON"}`

Run: `java GenerateJsonOrXmlReport template.docx data.json report-json.docx`

Data `data.xml`: `<root><Name>Aspose XML</Name></root>`

Run: `java GenerateJsonOrXmlReport template.docx data.xml report-xml.docx`

Text of `report-json.docx` (evaluation notices removed):

```text
Aspose JSON
```

Text of `report-xml.docx` (evaluation notices removed):

```text
Aspose XML
```

Result: **passed**: output contains the expected values

## linq-reporting-08: What is the difference between LINQ Reporting Engine and Mail Merge?

Result: **not applicable**: comparison only; no template or code to run

## rule-J1-right: error-correction.md J1 RIGHT example

Template:

```text
<<[sender.getName()]>>: <<[sender.getMessage()]>>
```

Run: `java GenerateReport `

Text of `report.docx` (evaluation notices removed):

```text
Aspose: Hello
```

Result: **passed**: output contains the expected values

## rule-J9-wrong: error-correction.md J9 WRONG example (must fail at run time)

Template:

```text
<<foreach [o in data.Orders.Where(x => x.Total > 100)]>>
<<[o.Name]>> — <<[o.Total]>>
<<end>>
```

Run: `java CreateReport `

Console output:

```text
Exception in thread "main" java.lang.IllegalArgumentException: A data source object must be of a visible type or implement 'interface java.lang.Iterable'.
Parameter name: dataSource
	at com.aspose.words.internal.zzo3.zzvc(Unknown Source)
	at com.aspose.words.internal.zzXcx.zzls(Unknown Source)
	at com.aspose.words.internal.zzXcx.zzls(Unknown Source)
	at com.aspose.words.internal.zzZII.zzls(Unknown Source)
	at com.aspose.words.internal.zzZII.zzls(Unknown Source)
	at com.aspose.words.ReportingEngine.buildReport(Unknown Source)
	at com.aspose.words.ReportingEngine.buildReport(Unknown Source)
	at CreateReport.main(CreateReport.java:9)
```

Result: **passed**: fails at run time as the rule says: Exception in thread "main" java.lang.IllegalArgumentException: A data source object must be of a visible type or implement 'interface java.lang.Iterable'.

## rule-J9-right: error-correction.md J9 RIGHT example

Template:

```text
<<foreach [o in data.getOrders().where(x => x.getTotal() > 100)]>>
<<[o.getName()]>> — <<[o.getTotal()]>>
<</foreach>>
```

Run: `java CreateReport `

Text of `report.docx` (evaluation notices removed):

```text
Notebook — 150
```

Result: **passed**: output contains the expected values
